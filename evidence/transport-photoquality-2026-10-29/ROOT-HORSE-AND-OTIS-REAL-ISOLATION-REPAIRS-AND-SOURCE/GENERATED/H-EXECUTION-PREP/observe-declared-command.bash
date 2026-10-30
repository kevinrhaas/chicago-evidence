# Passive outside observer for the exact native buildOne bash command only.
if [[ "${BASH_EXECUTION_STRING-}" == "${OTIS_ISO_DECLARED_COMMAND-}" && -n "${OTIS_ISO_DECLARED_COMMAND-}" ]]; then
  trap 'otis_iso_status=$?; printf "%s\n" "$otis_iso_status" > "$OTIS_ISO_COMMAND_RC"' EXIT
  exec > "$OTIS_ISO_COMMAND_LOG" 2>&1
fi
