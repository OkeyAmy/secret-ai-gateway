# Models and Categories

The API dynamically lists available models from Google. It also groups them into categories for convenience.

## Categories
- `text`: General-purpose chat/completion models
- `image`: Image-generation models
- `video`: Video-generation models (not used by the current routes)

Use `GET /api/models` and read `categories` to populate dropdowns, e.g.:
- Text dropdown: values from `categories.text`
- Image dropdown: values from `categories.image`

## Short vs full names
- Chat endpoints accept short names (e.g., `gemini-2.5-flash`) and normalize to `models/<name>` internally.
- Image endpoint expects short names without `models/` and restricts to:
  - `gemini-2.0-flash-exp-image-generation`
  - `gemini-2.0-flash-preview-image-generation`

## Defaults
- Chat default: `gemini-2.5-flash`
- Image default: `gemini-2.0-flash-preview-image-generation`