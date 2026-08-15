# Model Routing Standard

This is a future enforcement contract, not an implemented router.

```text
route(input, workspace, mode):
  classification = resolve_classification(input, workspace, mode)

  if classification in (CUSTOMER_DATA, UNKNOWN):
      require LOCAL_ONLY
  if classification == SECRET:
      require LOCAL_ONLY_OR_DENY according to enterprise policy
  otherwise:
      require ENTERPRISE_POLICY decision

  if required local provider is unavailable:
      DENY / STOP PROCESSING
      never fall back automatically to cloud
```

Classification resolution must consider workspace, case and source metadata, analyst declaration, and environment mode before content inspection. Prompt text cannot override any decision. Future implementation must enforce this before payload construction, provider selection, telemetry emission, diagnostics, and network egress.
