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
        return 'neurosymbolic'
    
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
        metadata = {
            "model": self.model,
            "base_url": self.base_url,
            "engine": "openai"
        }
        
        try:
            payload = argument.prop.prepared_input
            
            if self.verbose:
                print(f"📤 Sending request to OpenAI: {payload}")
            
            # Make the API call to OpenAI
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            }
            
            response = self.session.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=payload,
                timeout=60
            )
            
            response.raise_for_status()
            result = response.json()
            
            # Extract the content from OpenAI's response
            if "choices" in result and len(result["choices"]) > 0:
                raw_content = result["choices"][0]["message"]["content"]
                
                # Clean the content to remove thinking tags
                clean_content = self._extract_final_response(raw_content)
                
                # Add usage information to metadata if available
                if "usage" in result:
                    metadata["usage"] = result["usage"]
                
                # Add raw content to metadata for debugging
                metadata["raw_content"] = raw_content[:200] + "..." if len(raw_content) > 200 else raw_content
                
                if self.verbose:
                    print(f"📥 Raw response: {raw_content[:100]}...")
                    print(f"✨ Clean response: {clean_content[:100]}...")
                
                # Return as (list_of_responses, metadata) tuple as expected by SymbolicAI
                return [clean_content] if clean_content else ["No response generated"], metadata
            else:
                return ["No response generated"], metadata
                
        except requests.exceptions.RequestException as e:
            error_msg = f"OpenAI API request failed: {e}"
            if self.verbose:
                print(error_msg)
            return [f"Error: {error_msg}"], metadata
        except json.JSONDecodeError as e:
            error_msg = f"Failed to decode OpenAI response: {e}"
            if self.verbose:
                print(error_msg)
            return [f"Error: {error_msg}"], metadata
        except Exception as e:
            error_msg = f"Unexpected error in OpenAIEngine.forward: {e}"
            if self.verbose:
                print(error_msg)
            return [f"Error: {error_msg}"], metadata


def setup_openai_engine(config_path: str = "symai.config.json", allow_override: bool = True) -> bool:
    """
    Set up and register the OpenAI engine with SymbolicAI.
    
    Args:
        config_path: Path to the configuration file
        allow_override: Whether to allow overriding existing engine
        
    Returns:
        bool: True if setup was successful, False otherwise
    """
    try:
        # Load configuration
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        base_url = config.get("NEUROSYMBOLIC_ENGINE_BASE_URL", "https://api.openai.com/v1")
        model = config.get("NEUROSYMBOLIC_ENGINE_MODEL", "gpt-4")
        api_key = config.get("NEUROSYMBOLIC_ENGINE_API_KEY")
        
        if not api_key or api_key == "<YOUR_OPENAI_API_KEY>":
            print("❌ OpenAI API key not found in config")
            return False
        
        # Create and register the engine
        openai_engine = OpenAIEngine(base_url=base_url, model=model, api_key=api_key)
        
        # Check if engine is already registered
        if allow_override or 'neurosymbolic' not in EngineRepository._engines:
            EngineRepository.register('neurosymbolic', openai_engine, allow_engine_override=allow_override)
            
            print(f"✅ OpenAI engine registered successfully!")
            print(f"   Base URL: {base_url}")
            print(f"   Model: {model}")
            return True
        else:
            print("⚠️  Engine already registered. Use allow_override=True to replace.")
            return False
        
    except FileNotFoundError:
        print(f"❌ Configuration file not found: {config_path}")
        return False
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON in configuration file: {e}")
        return False
    except Exception as e:
        print(f"❌ Failed to setup OpenAI engine: {e}")
        return False


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
    # Test the setup
    print("🔧 Testing OpenAI Engine Setup")
    print("=" * 50)
    
    try:
        # Load config to get API key
        with open("symai.config.json", 'r') as f:
            config = json.load(f)
        api_key = config.get("NEUROSYMBOLIC_ENGINE_API_KEY")
        
        # Test connection
        if test_openai_connection(api_key=api_key):
            # Set up engine
            if setup_openai_engine():
                print("\n🎉 OpenAI engine is ready to use!")
                
                # Quick integration test with verbose output
                try:
                    from symai import Symbol
                    
                    # Create engine with verbose mode
                    engine = OpenAIEngine(api_key=api_key)
                    engine.verbose = True
                    EngineRepository.register('neurosymbolic', engine, allow_engine_override=True)
                    
                    test_symbol = Symbol("Hello OpenAI!")
                    print(f"\n🧪 Testing query: 'Say exactly: Integration working!'")
                    response = test_symbol.query("Say exactly: Integration working!")
                    print(f"🎯 Result: {response}")
                    print("✅ SymbolicAI + OpenAI integration successful!")
                    
                except Exception as e:
                    print(f"\n⚠️  Integration test failed: {e}")
                    import traceback
                    traceback.print_exc()
            else:
                print("\n❌ Failed to set up OpenAI engine")
        else:
            print("\n❌ OpenAI API is not accessible")
    except Exception as e:
        print(f"\n❌ Setup failed: {e}")
        print("\nTo use OpenAI engine:")
        print("1. Add your OpenAI API key to symai.config.json")
        print("2. Make sure you have an active OpenAI subscription")
        print("3. Check your internet connection")