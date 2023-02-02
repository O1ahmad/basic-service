{{/*
Expand service names containing embedded templates.
*/}}
{{- define "basic-service.name" -}}
{{- tpl .Values.name . -}}
{{- end -}}

{{/*
Expand service common names/FQDN containing embedded templates.
*/}}
{{- define "basic-service.commonName" -}}
{{- tpl .Values.common_name . -}}
{{- end -}}

{{/*
Expand service labels containing embedded templates.
*/}}
{{- define "basic-service.labels" -}}
{{- range  $key, $value := .Values.labels }}
{{ tpl $key $ }}: {{ tpl $value $ | quote}}
{{- end -}}
{{- end -}}

{{/*
Render correct CA Bundle for -cacert
*/}}
{{- define "returnCACertificates" }}
  {{- if eq . "VaultCAs" }}
  {{ template "_returnVaultCA" }}
  {{- end }}
  {{- if eq . "VaultAndBastionCAs" }}
  {{ template "_returnVaultCA" }}
  {{ template "_returnBastionCA" }}
  {{- end }}
{{- end }}
