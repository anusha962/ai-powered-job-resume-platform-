"""A flat taxonomy of common tech skills/keywords used for extraction & matching.
Kept as a plain list (not a heavy NLP model) so the app stays lightweight to
deploy on Render's free tier. Extend this list as needed for your domain.
"""

SKILL_TAXONOMY = [
    # Languages
    "python", "java", "javascript", "typescript", "c++", "c#", "go", "golang",
    "rust", "php", "ruby", "kotlin", "swift", "scala", "r", "matlab", "sql",
    "html", "css", "bash", "shell scripting",
    # Web / Frontend
    "react", "react.js", "redux", "vue", "vue.js", "angular", "next.js",
    "svelte", "tailwind", "tailwind css", "bootstrap", "jquery", "webpack",
    "vite", "sass", "graphql",
    # Backend / Frameworks
    "django", "django rest framework", "flask", "fastapi", "spring",
    "spring boot", "express", "express.js", "node.js", "nestjs", "rails",
    "laravel", ".net", "asp.net",
    # Data / ML / AI
    "machine learning", "deep learning", "nlp", "natural language processing",
    "llm", "large language models", "rag", "retrieval augmented generation",
    "transformers", "pytorch", "tensorflow", "keras", "scikit-learn",
    "pandas", "numpy", "opencv", "computer vision", "huggingface",
    "prompt engineering", "langchain", "vector databases", "embeddings",
    "data analysis", "data science", "data engineering", "etl",
    "spark", "hadoop", "airflow",
    # Databases
    "mysql", "postgresql", "postgres", "mongodb", "redis", "sqlite",
    "elasticsearch", "dynamodb", "cassandra", "oracle", "firebase",
    # Cloud / DevOps
    "aws", "azure", "gcp", "google cloud", "docker", "kubernetes",
    "terraform", "ansible", "jenkins", "ci/cd", "github actions",
    "linux", "nginx", "microservices", "serverless", "lambda",
    "ec2", "s3", "cloudformation",
    # Tools / Practices
    "git", "github", "gitlab", "jira", "agile", "scrum", "rest api",
    "restful apis", "api development", "unit testing", "pytest",
    "test driven development", "tdd", "object oriented programming", "oop",
    "system design", "design patterns", "websockets", "celery",
    # Mobile
    "android", "ios", "react native", "flutter",
    # Soft / role-adjacent (kept light)
    "project management", "communication", "leadership", "problem solving",
]
