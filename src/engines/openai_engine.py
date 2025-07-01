#!/usr/bin/env python3
"""
Custom OpenAI Engine for SymbolicAI
==================================

This module provides an OpenAI-compatible engine implementation for SymbolicAI
that works with OpenAI's API and compatible providers.
"""

import json
import re
import requests
from typing import Dict, Any, Optional, Tuple, List
from symai.backend.base import Engine
from symai.functional import EngineRepository
from symai.backend.settings import SYMAI_CONFIG


class OpenAIEngine(Engine):
    """
    Custom engine for OpenAI API and compatible providers.
    
    This engine translates SymbolicAI requests to OpenAI's API format,
    supporting both OpenAI and compatible providers like Azure OpenAI,
    local deployments, etc.
    """
    
    def __init__(self, base_url: str = "https://api.openai.com/v1", 
                 model: str = "gpt-4", 
                 api_key: str = None):
        # Initialize the parent Engine class
        super().__init__()
        
        self.base_url = base_url.rstrip('/')
        self.model = model
        self.api_key = api_key
        self.session = requests.Session()
        
        # Initialize required attributes for SymbolicAI
        self.time_clock = False
        self.verbose = False
        
    def id(self) -> str:
        """Return the engine identifier."""
        return 'openai-comp'
    
    def _extract_final_response(self, content: str) -> str:
        """
        Extract the final response from content that may contain thinking tags.
        
        Args:
            content: Raw content from the model that may contain <think>...</think> tags
            
        Returns:
            str: Clean response without thinking tags
        """
        if not content:
            return content
        
        # Remove <think>...</think> blocks (including nested ones)
        think_pattern = r'<think>.*?</think>'
        
        # Remove all thinking blocks
        cleaned = re.sub(think_pattern, '', content, flags=re.DOTALL)
        
        # Clean up extra whitespace
        cleaned = cleaned.strip()
        
        # If nothing is left after removing think tags, return original
        if not cleaned and content:
            # Fallback: try to find content after the last </think>
            last_think_end = content.rfind('</think>')
            if last_think_end != -1:
                cleaned = content[last_think_end + 8:].strip()
            else:
                # No think tags found, return original
                cleaned = content.strip()
        
        return cleaned
    
    def prepare(self, argument):
        """
        Prepare the input for the OpenAI API call.
        
        Args:
            argument: Contains preprocessed input, args, kwargs, and properties
        """
        try:
            # Get the input from SymbolicAI - check multiple possible locations
            prompts = None
            
            # Try different input sources in order of preference
            if hasattr(argument.prop, 'preprocessed_input') and argument.prop.preprocessed_input:
                prompts = argument.prop.preprocessed_input
            elif hasattr(argument.prop, 'processed_input') and argument.prop.processed_input:
                prompts = argument.prop.processed_input
            elif hasattr(argument.prop, 'instance') and argument.prop.instance:
                # Fallback to instance content
                context = argument.kwargs.get('context', '')
                if context:
                    prompts = f"Data: {argument.prop.instance}\nContext: {context}\nAnswer:"
                else:
                    prompts = str(argument.prop.instance)
            else:
                prompts = "Please provide a helpful response."
            
            kwargs = argument.kwargs
            
            if self.verbose:
                print(f"  📝 Found prompts: {repr(prompts)}")
            
            # Handle different input formats
            if isinstance(prompts, list):
                if len(prompts) == 1:
                    # Single message
                    if isinstance(prompts[0], dict):
                        messages = [prompts[0]]
                    else:
                        messages = [{"role": "user", "content": str(prompts[0])}]
                else:
                    # Multiple messages - assume they're already formatted
                    messages = []
                    for prompt in prompts:
                        if isinstance(prompt, dict):
                            messages.append(prompt)
                        else:
                            messages.append({"role": "user", "content": str(prompt)})
            elif isinstance(prompts, str):
                messages = [{"role": "user", "content": prompts}]
            else:
                messages = [{"role": "user", "content": str(prompts)}]
            
            # Prepare the request payload for OpenAI's API
            payload = {
                "model": self.model,
                "messages": messages,
                "temperature": kwargs.get("temperature", 0.7),
                "max_tokens": kwargs.get("max_tokens", 2000),
                "stream": False
            }
            
            # Add any additional parameters supported by OpenAI
            if "top_p" in kwargs:
                payload["top_p"] = kwargs["top_p"]
            if "frequency_penalty" in kwargs:
                payload["frequency_penalty"] = kwargs["frequency_penalty"]
            if "presence_penalty" in kwargs:
                payload["presence_penalty"] = kwargs["presence_penalty"]
            if "stop" in kwargs:
                payload["stop"] = kwargs["stop"]
                
            argument.prop.prepared_input = payload
            
        except Exception as e:
            if self.verbose:
                print(f"Error in OpenAIEngine.prepare: {e}")
            # Fallback preparation
            argument.prop.prepared_input = {
                "model": self.model,
                "messages": [{"role": "user", "content": "Please provide a helpful response."}],
                "temperature": 0.7,
                "max_tokens": 2000,
                "stream": False
            }
    
    def forward(self, argument) -> Tuple[List[str], Dict[str, Any]]:
        """
        Execute the API call to OpenAI.
        
        Args:
            argument: Contains the prepared input and other properties
            
        Returns:
            Tuple[List[str], Dict]: (list_of_responses, metadata) as expected by SymbolicAI
        """
        # Initialize metadata with basic info
        metadata = {
            "model": self.model,
            "base_url": self.base_url,
            "engine": self.id()
        }

        try:
            # Get prepared payload
            payload = argument.prop.prepared_input
            if self.verbose:
                print(f"📤 Sending request to OpenAI: {payload}")

            # Prepare headers
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            }

            # Make API call
            response = self.session.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=payload,
                timeout=60
            )

            # Check for HTTP errors
            try:
                response.raise_for_status()
            except requests.exceptions.HTTPError as e:
                if response.status_code == 401:
                    error_msg = "Authentication failed. Please check your API key."
                else:
                    error_msg = f"API request failed (HTTP {response.status_code}): {str(e)}"
                if self.verbose:
                    print(error_msg)
                return [f"Error: {error_msg}"], {
                    "error": True,
                    "status": "api_error",
                    "http_status": response.status_code,
                    **metadata
                }

            # Parse JSON response
            try:
                result = response.json()
            except json.JSONDecodeError as e:
                error_msg = f"Failed to decode API response: {str(e)}"
                if self.verbose:
                    print(error_msg)
                return [f"Error: {error_msg}"], {
                    "error": True,
                    "status": "invalid_response",
                    **metadata
                }

            # Process successful response
            if "choices" in result and len(result["choices"]) > 0:
                raw_content = result["choices"][0]["message"]["content"]
                clean_content = self._extract_final_response(raw_content)

                # Update metadata
                if "usage" in result:
                    metadata["usage"] = result["usage"]
                metadata["raw_content"] = raw_content[:200] + "..." if len(raw_content) > 200 else raw_content

                if self.verbose:
                    print(f"📥 Raw response: {raw_content[:100]}...")
                    print(f"✨ Clean response: {clean_content[:100]}...")

                if clean_content:
                    return [clean_content], metadata
                else:
                    return ["Error: No valid response generated"], {
                        "error": True,
                        "status": "empty_response",
                        **metadata
                    }
            else:
                return ["Error: No response content"], {
                    "error": True,
                    "status": "no_content",
                    **metadata
                }

        except requests.exceptions.RequestException as e:
            error_msg = f"API connection error: {str(e)}"
            if self.verbose:
                print(error_msg)
            return [f"Error: {error_msg}"], {
                "error": True,
                "status": "connection_error",
                **metadata
            }

        except Exception as e:
            error_msg = f"Unexpected error: {str(e)}"
            if self.verbose:
                print(error_msg)
            return [f"Error: {error_msg}"], {
                "error": True,
                "status": "internal_error",
                **metadata
            }



def test_openai_connection(base_url: str = "https://api.openai.com/v1", api_key: str = None) -> bool:
    """
    Test if OpenAI API is accessible.
    
    Args:
        base_url: The base URL for OpenAI's API
        api_key: OpenAI API key to use for testing
        
    Returns:
        bool: True if OpenAI is accessible, False otherwise
    """
    try:
        if not api_key:
            print("❌ OpenAI API key not provided")
            return False
            
        headers = {
            "Authorization": f"Bearer {api_key}"
        }
        
        response = requests.get(f"{base_url.rstrip('/')}/models", headers=headers, timeout=5)
        if response.status_code == 200:
            print("✅ OpenAI API is accessible")
            return True
        else:
            print(f"⚠️  OpenAI API responded with status code: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Cannot connect to OpenAI API: {e}")
        return False


if __name__ == "__main__":
    # Test the setup using EngineManager
    print("🔧 Testing OpenAI Engine Setup")
    print("=" * 50)
    
    try:
        from engine_manager import EngineManager
        from symai import Symbol
        
        # Set up engine through manager
        if EngineManager.setup_engine('openai-comp'):
            print("\n🎉 OpenAI-compatible engine is ready to use!")
            
            # Quick integration test
            test_symbol = Symbol("Hello OpenAI!")
            print(f"\n🧪 Testing query: 'Say exactly: Integration working!'")
            response = test_symbol.query("Say exactly: Integration working!")
            print(f"🎯 Result: {response}")
            print("✅ SymbolicAI + OpenAI integration successful!")
            
    except Exception as e:
        print(f"\n❌ Setup failed: {e}")
        print("\nTo use OpenAI engine:")
        print("1. Add your OpenAI API key to symai.config.json")
        print("2. Make sure you have an active OpenAI subscription")
        print("3. Check your internet connection")