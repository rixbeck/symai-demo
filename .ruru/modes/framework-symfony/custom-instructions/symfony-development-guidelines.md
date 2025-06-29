# Symfony Development Guidelines

## Core Principles

### 1. Follow Symfony Best Practices
- Use Symfony's recommended directory structure (`src/`, `config/`, `templates/`, `tests/`)
- Follow PSR-4 autoloading standards
- Use dependency injection instead of static calls
- Leverage Symfony's component architecture

### 2. Configuration Management
- Prefer YAML for configuration files (services, routes, security)
- Use environment variables for environment-specific settings
- Organize configuration files logically in `config/packages/`
- Use `config/services.yaml` for custom service definitions

### 3. Controller Best Practices
- Keep controllers thin - delegate business logic to services
- Use type hints and return type declarations
- Use dependency injection in constructors or method arguments
- Return Response objects or use Symfony's view layer

### 4. Service Layer
- Create services for business logic
- Use dependency injection for service dependencies
- Make services stateless when possible
- Use interfaces for better testability

### 5. Database with Doctrine
- Use entities with proper annotations/attributes
- Create custom repository methods for complex queries
- Use migrations for schema changes
- Implement proper relationships between entities

## Common Symfony Patterns

### Controller Pattern
```php
#[Route('/posts', name: 'post_')]
class PostController extends AbstractController
{
    public function __construct(
        private PostService $postService
    ) {}

    #[Route('/', name: 'index', methods: ['GET'])]
    public function index(): Response
    {
        $posts = $this->postService->getAllPosts();
        
        return $this->render('post/index.html.twig', [
            'posts' => $posts,
        ]);
    }
}
```

### Service Pattern
```php
#[AsService]
class PostService
{
    public function __construct(
        private PostRepository $postRepository,
        private EntityManagerInterface $entityManager
    ) {}

    public function createPost(array $data): Post
    {
        $post = new Post();
        // ... set data
        
        $this->entityManager->persist($post);
        $this->entityManager->flush();
        
        return $post;
    }
}
```

### Entity Pattern
```php
#[ORM\Entity(repositoryClass: PostRepository::class)]
#[ORM\Table(name: 'posts')]
class Post
{
    #[ORM\Id]
    #[ORM\GeneratedValue]
    #[ORM\Column(type: 'integer')]
    private ?int $id = null;

    #[ORM\Column(type: 'string', length: 255)]
    private string $title;

    #[ORM\Column(type: 'text')]
    private string $content;

    #[ORM\Column(type: 'datetime_immutable')]
    private \DateTimeImmutable $createdAt;

    // getters and setters...
}
```

## Testing Guidelines

### Unit Tests
- Test services and business logic
- Mock dependencies using PHPUnit mocks
- Use data providers for multiple test scenarios

### Functional Tests
- Test controllers and HTTP responses
- Use Symfony's WebTestCase
- Test authentication and authorization

### Integration Tests
- Test database interactions
- Use test database with fixtures
- Test complete workflows

## Performance Considerations

### Doctrine Optimization
- Use `SELECT` clauses to limit fetched data
- Implement proper eager/lazy loading
- Use Doctrine's query cache
- Monitor query performance with Symfony Profiler

### Symfony Optimization
- Use Symfony's HTTP cache
- Implement proper caching strategies
- Optimize autoloading for production
- Use OpCache in production

## Security Best Practices

### Authentication & Authorization
- Use Symfony Security component
- Implement proper user providers
- Use voters for complex authorization logic
- Validate and sanitize all input

### Data Protection
- Use CSRF protection for forms
- Implement proper input validation
- Use parameterized queries (Doctrine handles this)
- Follow OWASP security guidelines