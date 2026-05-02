"""
Shared structure contract for 04-generate/.
"""

REQUIRED_GENERATED_SUBDIRS = (
    "overview",
    "pages",
    "rules",
    "data",
    "acceptance",
    "agent-context",
)

REQUIRED_GENERATED_FILES = {
    "overview": ("project-overview.md",),
    "agent-context": (
        "frontend-context.md",
        "backend-context.md",
        "test-context.md",
        "product-review-context.md",
    ),
}
