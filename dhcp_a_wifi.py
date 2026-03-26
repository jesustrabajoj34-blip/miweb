import subprocess

INTERFAZ = "Ethernet"

IP_FIJA = "169.254.255.100"
MASCARA = "24"  # equivalente a 255.255.255.0


def ejecutar_ps(comando):
    try:
        subprocess.run(
            ["powershell", "-Command", comando],
            check=True
        )
    except subprocess.CalledProcessError as e:
        print("Error ejecutando PowerShell:", e)


def es_dhcp():
    comando = f"(Get-NetIPInterface -InterfaceAlias '{INTERFAZ}' -AddressFamily IPv4).Dhcp"
    resultado = subprocess.run(
        ["powershell", "-Command", comando],
        capture_output=True,
        text=True
    )

    return "Enabled" in resultado.stdout


def poner_dhcp():
    print("→ Activando DHCP...")
    ejecutar_ps(f"Set-NetIPInterface -InterfaceAlias '{INTERFAZ}' -Dhcp Enabled")
    ejecutar_ps(f"Set-DnsClientServerAddress -InterfaceAlias '{INTERFAZ}' -ResetServerAddresses")


def poner_ip_fija():
    print("→ Configurando IP fija...")

    # Elimina IPs previas
    ejecutar_ps(f"Remove-NetIPAddress -InterfaceAlias '{INTERFAZ}' -Confirm:$false -ErrorAction SilentlyContinue")

    # Asigna nueva IP
    ejecutar_ps(
        f"New-NetIPAddress -InterfaceAlias '{INTERFAZ}' -IPAddress {IP_FIJA} -PrefixLength {MASCARA}"
    )


def main():
    if es_dhcp():
        print("Actualmente en DHCP")
        poner_ip_fija()
    else:
        print("Actualmente en IP fija")
        poner_dhcp()

    print("✔ Cambio completado")


if __name__ == "__main__":
    main()