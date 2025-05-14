call nssm.exe install wrldc_edna_grafana_api "%cd%\run_server.bat"
call nssm.exe set wrldc_edna_grafana_api AppStdout "%cd%\logs\wrldc_edna_grafana_api.log"
call nssm.exe set wrldc_edna_grafana_api AppStderr "%cd%\logs\wrldc_edna_grafana_api.log"
call nssm.exe set wrldc_edna_grafana_api AppRotateFiles 1
call nssm.exe set wrldc_edna_grafana_api AppRotateOnline 1
call nssm.exe set wrldc_edna_grafana_api AppRotateSeconds 86400
call nssm.exe set wrldc_edna_grafana_api AppRotateBytes 104857600