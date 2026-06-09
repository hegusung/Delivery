# Delivery

This project works with Mythic C2 and aims to create containers responsible of creating infection chains within Mythic

## Payload Types

- Wrappers: Wrappers are payloads which includes/pack/contains another payload
- Downloaders: Downloaders are payloads which downloads another payload from a url and processes it

Downloaders currently doesn't exist within mythic, they work my specifying a URL parameter

## Install

All the containers can be installed all at once using the following command:

```sh
./mythic-cli install github https://github.com/hegusung/Delivery
``` 

## Payloads

Currently the following payloads are implemented:

### Binaries

- dotnet_wraps_csharp

### Scripts

- jscript_download_save_execute
- encoded_script
- psh_remote_psh
- psh_wraps_shellcode
- wsf_remote_script
- wsf_wraps_script

### File formats

- inf_remote_sct
- inf_wraps_cmd
- csharp_wraps_shellcode
- csproj_wraps_shellcode
- sct_wraps_script
- sct_remote_script
- xsl_wraps_script
- hta_wraps_script
- lnk_wraps_cmd
- reg_wraps_cmd

### LOLBas

- cmd_wraps_powershell
- lolbas_exec_dotnet
- lolbas_exec_csproj
- cmd_advpack_local_inf
- cmd_cmstp_local_inf
- cmd_infdefaultinstall_local_inf
- cmd_regsvr32_remote_sct
- cmd_setupapi_local_inf

### Archives

- packmypayload

### Phishing kits

- clickfix
- filefix
- html_smuggling
- svg_smuggling
- clickonce_wraps_csharp

### NetNTLM auth

- lnk_smb_auth
- scf_smb_auth

### Other

- url_payload
