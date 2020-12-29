from pathlib import Path
import json
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
import getpass

from paramiko import SSHClient
from scp import SCPClient


RM_TEMPLATES_DIR = Path("/usr/share/remarkable/templates/")


def main(args):
    ssh = SSHClient()
    ssh.load_system_host_keys()

    password = getpass.getpass() if args.password else None
    ssh.connect(args.host, username=args.user, password=password)

    scp = SCPClient(ssh.get_transport())

    # Get templates.json from remarkable
    scp.get(str(RM_TEMPLATES_DIR / "templates.json"))
    with Path("./templates.json").open("r") as f:
        templates = json.load(f)

    # Load new/updated templates
    with Path("./files/templates.json").open("r") as f:
        new_templates = json.load(f)

    # Updated templates.json
    new_template_names = [template["name"] for template in new_templates["templates"]]
    for i, template in enumerate(templates["templates"]):
        for new_template in new_templates["templates"]:
            if template["name"] == new_template["name"]:
                templates["templates"][i] = new_template
                new_template_names.remove(template["name"])

    for template in new_templates["templates"]:
        if template["name"] in new_template_names:
            templates["templates"].append(template)

    with Path("./templates.json").open("w") as f:
        json.dump(templates, f, indent=2)

    # Copy files to remarkable
    files = ["templates.json"]
    for ext in ["png", "svg"]:
        files += [f"./files/{filename}.{ext}" for filename in [template["filename"] for template in new_templates["templates"]]]
    scp.put(files, remote_path=str(RM_TEMPLATES_DIR))

    # Restart xochitl
    stdin, stdout, stderr = ssh.exec_command('systemctl restart xochitl')

    if errors := stderr.readlines():    
        raise Exception("\n".joins(errors))
    
    if out := stdout.readlines():
        for line in out:
            print(line)

    ssh.close()    

if __name__ == "__main__":
    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument("--host", type=str, default="10.11.99.1", help="Hostname for connecting with remarkable")
    parser.add_argument("-u", "--user", type=str, default="root", help="Username for connecting with remarkable")
    parser.add_argument("-p", "--password", action="store_true", help="Use ssh password for connection with remarkable")
    args = parser.parse_args()
    main(args)