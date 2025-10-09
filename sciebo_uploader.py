import os
import json
import requests
import streamlit as st
from config import UPLOAD_FOLDER,SCIEBO_USERNAME,SCIEBO_PASSWORD,SCIEBO_APPNAME,SCIEBO_IMAGE_BASEURL,SCIEBO_STATE_BASEURL,STATE_FOLDER     # Import upload directory from config


class Sciebo:
    """
    Sciebo WebDAV Handler Class to upload images and session state data.
    """

    # Sciebo WebDAV Credentials
    SCIEBO_USERNAME =SCIEBO_USERNAME
    SCIEBO_PASSWORD = SCIEBO_PASSWORD # this is app password
    SCIEBO_APPNAME = SCIEBO_APPNAME
    SCIEBO_IMAGE_BASEURL = SCIEBO_IMAGE_BASEURL
    SCIEBO_STATE_BASEURL = SCIEBO_STATE_BASEURL

    @classmethod
    def upload_image(cls, file_path,uuid):
        """
        Uploads an image to the Sciebo directory 'medical_ai/images/'.

        :param file_path: Local path of the image to be uploaded.
        """
        if not os.path.exists(file_path):
            st.error("❌ File not found: " + file_path)
            return

        file_name = os.path.basename(file_path)
        file_extension = os.path.splitext(file_path)[1]
        # ✅ Ensure trailing slash before adding filename
        sciebo_url = f"{cls.SCIEBO_IMAGE_BASEURL.rstrip('/')}/r_vc_{uuid}{file_extension}"

        try:
            with open(file_path, "rb") as file:
                print("UUID of Image: ",uuid)
                print("Sciebo URL of Image: ",sciebo_url)
                # ✅ Use data= instead of files= for WebDAV PUT
                response = requests.put(
                    sciebo_url,
                    data=file,
                    auth=(cls.SCIEBO_USERNAME, cls.SCIEBO_PASSWORD),
                )

            if response.status_code in [201, 204]:
                pass
            else:
                st.error(f"❌ Failed Image: {response.status_code}")
                print(response.text)

        except Exception as e:
            st.error(f"⚠️ Error image: {str(e)}")

    @classmethod
    def upload_state_data(cls,uuid):

        if not uuid:
            st.error("❌ User UUID not found in session state.")
            return

        user_uuid = uuid

        json_file_name = f"{user_uuid}.json"
        json_file_path = os.path.join(STATE_FOLDER, json_file_name)

        try:
            # Convert session state to JSON
            # Upload to Sciebo
            # ✅ Ensure trailing slash before adding filename
            sciebo_url = f"{cls.SCIEBO_STATE_BASEURL.rstrip('/')}/r_vc_{json_file_name}"
            print("=== Debug Info ===")
            print("Username:", cls.SCIEBO_USERNAME)
            print("Password set?", bool(cls.SCIEBO_PASSWORD))
            print("File path exists?", os.path.exists(json_file_path))
            print("File path:", json_file_path)
            print("Uploading to URL:", sciebo_url)






            with open(json_file_path, "rb") as file:
                print("UUID of State: ",uuid)
                print("Sciebo URL of State: ",sciebo_url)
                # ✅ Use data= instead of files=
                response = requests.put(
                    sciebo_url,
                    data=file,
                    auth=(cls.SCIEBO_USERNAME, cls.SCIEBO_PASSWORD),
                )
            print("Response status code:", response.status_code)
            print("Response text:", response.text)



            if response.status_code in [201, 204]:
                pass
            else:
                st.error(f"❌ Failed session: {response.status_code} {response.text}")

        except Exception as e:
            st.error(f"⚠️ Error session state: {str(e)}")
