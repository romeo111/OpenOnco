# Clinical Question Skill

Status: draft implementation

## Goal

Let a clinician or trainee paste an oncology vignette in natural language and
receive one of three outputs:

- an answer grounded in an OpenOnco engine result;
- several plausible alternatives when the engine exposes them;
- clarifying questions when the case is underspecified or outside current KB
  coverage.

## Boundary

The LLM is not a clinical decision-maker. It has two allowed jobs:

1. Extract a structured OpenOnco patient profile from free text.
2. Present the deterministic engine output in a concise tumor-board answer.

The treatment or diagnostic pathway comes from `generate_plan()`,
`generate_diagnostic_brief()`, and `orchestrate_mdt()`. If those fail to
produce a result, the response must be `needs_clarification` or `unsupported`.

## Site Flow

`/ask.html` posts:

```json
{
  "case_text": "free-text clinical vignette",
  "locale": "uk",
  "user_id": "browser-generated anonymous id"
}
```

to `/api/clinical-question`.

The server adapter:

1. runs a preflight guard before any OpenAI call:
   - blocks prompt-injection style requests;
   - asks for clarification when the text is not an oncology vignette;
   - rejects overly long pasted material;
2. calls OpenAI Structured Outputs to extract:
   - `patient_profile_json`;
   - `clinical_question`;
   - answer options, if present;
   - mentioned biomarkers and drugs;
   - missing profile fields;
3. validates extracted biomarkers and drugs against the OpenOnco KB vocabulary;
4. parses `patient_profile_json`;
5. runs the local OpenOnco engine;
6. calls OpenAI Structured Outputs again to map the engine summary to a concise
   answer or clarification request.

If a biomarker or drug mention cannot be mapped to the KB vocabulary, the
server returns `needs_clarification` and does not run the engine. This prevents
fake biomarker IDs, invented drug names, and LLM-mapped unknowns from entering
the treatment selection path.

The page shows three example prompts and keeps a local browser counter. The
server also enforces `MAX_QUESTIONS_PER_USER = 3` for each `user_id`. The
current draft stores that count in process memory, which is enough for local
testing and a simple server runtime. A production serverless deploy should move
the counter to persistent storage, such as KV or a session-backed table, if the
quota must survive cold starts and horizontal scaling.

The browser never sees `OPENAI_API_KEY`.

## Deployment

Environment variables:

- `OPENAI_API_KEY`: required on the server;
- `OPENAI_MODEL`: optional, defaults to `gpt-5.2`;
- `OPENONCO_ALLOWED_ORIGIN`: optional CORS origin, defaults to `*`;
- `OPENONCO_DEBUG=1`: optional stack traces in JSON errors.

Use a dedicated OpenAI project key for this endpoint, not a personal reusable
key. For local testing, copy `.env.example` to `.env` and replace
`OPENAI_API_KEY`. For deployment, add the same variables in the hosting
provider's serverless environment settings. Do not expose the key in
`docs/ask.html`, frontend JavaScript, GitHub Pages settings, or any public
config file.

The adapter is stdlib-only for OpenAI transport and intentionally does not
`import openai`, matching the project rule that active clinical skill modules
must not contain LLM clients.

## OpenAI API Notes

The implementation uses the Responses API with `text.format.type =
"json_schema"` and `strict = true`, following OpenAI's Structured Outputs
guidance. JSON mode is intentionally avoided because it validates JSON syntax
but does not guarantee schema adherence.
