import streamlit as st
import json
import os
import random
import string
from datetime import datetime
import pandas as pd

class JSONFileManager:
    def __init__(self, base_directory='data'):
        """
        Initialize the JSON File Manager with structured directory
        
        :param base_directory: Base directory for data storage
        """
        self.base_directory = base_directory
        self.platforms = ["twitter", "facebook", "instagram", "linkedin"]
        
        # Create base directory and platform subdirectories
        os.makedirs(base_directory, exist_ok=True)
        for platform in self.platforms:
            platform_path = os.path.join(base_directory, platform, "posts_queue")
            os.makedirs(platform_path, exist_ok=True)
    
    def generate_unique_id(self):
        """
        Generate a unique 8-digit numerical ID
        
        :return: 8-digit unique ID as string
        """
        while True:
            # Generate 8-digit ID
            new_id = ''.join(random.choices(string.digits, k=8))
            
            # Check if ID is already in use
            if not self.id_exists(new_id):
                return new_id
    
    def id_exists(self, id_to_check):
        """
        Check if an ID already exists in any platform's posts_queue
        
        :param id_to_check: ID to verify
        :return: Boolean indicating if ID exists
        """
        for platform in self.platforms:
            platform_path = os.path.join(self.base_directory, platform, "posts_queue")
            for filename in os.listdir(platform_path):
                if filename.startswith(id_to_check):
                    return True
        return False
    
    def list_files(self):
        """
        Recursively list all JSON files across platforms
        
        :return: List of JSON filenames with their relative paths
        """
        json_files = []
        for platform in self.platforms:
            platform_path = os.path.join(self.base_directory, platform, "posts_queue")
            for file in os.listdir(platform_path):
                if file.endswith('.json'):
                    relative_path = os.path.join(platform, "posts_queue", file)
                    json_files.append(relative_path)
        return json_files
    
    def get_filename_only(self, filepath):
        """
        Extract just the filename from a full path
        
        :param filepath: Full or relative path of the file
        :return: Filename without path
        """
        return os.path.basename(filepath)
    
    def read_file(self, filename):
        """
        Read a JSON file
        
        :param filename: Relative path of the file to read
        :return: Parsed JSON content
        """
        filepath = os.path.join(self.base_directory, filename)
        with open(filepath, 'r') as f:
            return json.load(f)
    
    def save_file(self, data):
        """
        Save JSON data to a file in the appropriate platform folder
        
        :param data: Dictionary to save
        :return: Filename of the saved file
        """
        # Validate platform
        platform = data.get("platform", "").lower()
        if platform not in self.platforms:
            raise ValueError(f"Invalid platform. Must be one of {self.platforms}")
        
        # Use ID as filename
        id_val = data.get("id")
        if not id_val:
            # Generate new ID if not provided
            id_val = self.generate_unique_id()
            data["id"] = id_val
        
        # Construct filename and path
        filename = f"{id_val}.json"
        filepath = os.path.join(self.base_directory, platform, "posts_queue", filename)
        
        # Save file
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        
        return filename
    
    def delete_file(self, filename):
        """
        Delete a JSON file
        
        :param filename: Relative path of the file to delete
        """
        filepath = os.path.join(self.base_directory, filename)
        os.remove(filepath)

def main():
    st.title("Content Manager")
    
    # Initialize file manager
    file_manager = JSONFileManager()
    
    # Get files and create a mapping of display names to full paths
    files = file_manager.list_files()
    file_display_names = [file_manager.get_filename_only(f) for f in files]
    
    # Create a dictionary to map display names back to full paths
    file_name_to_path = dict(zip(file_display_names, files))
    
    # Sidebar for file operations
    st.sidebar.header("Content Operations")
    
    # File selection with display names
    selected_display_name = st.sidebar.selectbox(
        "Select post", 
        ["Create New"] + file_display_names
    )
    
    # Get the full path if a file is selected
    selected_file = file_name_to_path.get(selected_display_name) if selected_display_name != "Create New" else "Create New"
    
    # Platforms list
    platforms = ["twitter", "facebook", "instagram", "linkedin"]
    
    # Initialize session state for form
    if 'form_data' not in st.session_state:
        st.session_state.form_data = {
            "platform": "twitter",
            "id": file_manager.generate_unique_id(),
            "content": "",
            "hashtags": "",
            "datetime_for_post": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    
    # Handling file selection
    if selected_file != "Create New":
        # Load existing file data
        loaded_data = file_manager.read_file(selected_file)
        
        # Ensure platform is valid
        loaded_platform = loaded_data.get("platform", "twitter")
        if loaded_platform not in platforms:
            loaded_platform = "twitter"
        
        st.session_state.form_data = {
            "platform": loaded_platform,
            "id": loaded_data.get("id", ""),
            "content": loaded_data.get("content", ""),
            "hashtags": loaded_data.get("hashtags", ""),
            "datetime_for_post": loaded_data.get("datetime_for_post", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        }
    
    # Form for editing/creating JSON
    with st.form(key='json_form'):
        st.header("Post Details")
        
        # Platform selection
        platform = st.selectbox(
            "Platform", 
            platforms, 
            index=platforms.index(st.session_state.form_data.get("platform", "twitter"))
        )
        
        # ID field (read-only)
        id_val = st.text_input(
            "ID (Unique 8-digit Identifier)", 
            value=st.session_state.form_data.get("id", ""),
            disabled=True
        )
        
        content = st.text_area(
            "Content", 
            value=st.session_state.form_data.get("content", "")
        )
        
        hashtags = st.text_input(
            "Hashtags", 
            value=st.session_state.form_data.get("hashtags", "")
        )
        
        datetime_for_post = st.text_input(
            "Datetime for Post (ISO Format)", 
            value=st.session_state.form_data.get("datetime_for_post", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        )
        
        # Buttons
        col1, col2, col3 = st.columns(3)
        
        save_button = col1.form_submit_button("Save File")
        delete_button = col2.form_submit_button("Delete File")
        new_button = col3.form_submit_button("Create New")
        
        # Handle form submission
        if save_button:
            # Prepare data
            data = {
                "platform": platform,
                "id": id_val,
                "content": content,
                "hashtags": hashtags,
                "datetime_for_post": datetime_for_post
            }
            
            try:
                # Save file 
                saved_filename = file_manager.save_file(data)
                st.success(f"File saved: {saved_filename}")
                st.rerun()
            except ValueError as e:
                st.error(str(e))
        
        if delete_button and selected_file != "Create New":
            file_manager.delete_file(selected_file)
            st.success(f"File {selected_file} deleted")
            st.rerun()
        
        if new_button:
            # Reset form data with new unique ID
            st.session_state.form_data = {
                "platform": "twitter",
                "id": file_manager.generate_unique_id(),
                "content": "",
                "hashtags": "",
                "datetime_for_post": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            st.rerun()
    
    # File Listing and Filtering
    st.header("JSON Files List")
    
    # Convert files to DataFrame for sorting and filtering
    file_data = []
    for filename in files:
        data = file_manager.read_file(filename)
        data['filename'] = filename
        file_data.append(data)
    
    if file_data:
        df = pd.DataFrame(file_data)
        
        # Sorting
        sort_by = st.selectbox(
            "Sort By", 
            ["datetime_for_post", "platform", "id"]
        )
        sort_order = st.radio("Sort Order", ["Ascending", "Descending"])
        
        # Filtering
        st.subheader("Filters")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            content_filter = st.text_input("Filter by Content")
        
        with col2:
            hashtag_filter = st.text_input("Filter by Hashtags")
        
        with col3:
            platform_filter = st.selectbox(
                "Filter by Platform", 
                ["All"] + platforms
            )
        
        # Apply filters
        filtered_df = df.copy()
        if content_filter:
            filtered_df = filtered_df[filtered_df['content'].str.contains(content_filter, case=False)]
        
        if hashtag_filter:
            filtered_df = filtered_df[filtered_df['hashtags'].str.contains(hashtag_filter, case=False)]
        
        if platform_filter != "All":
            filtered_df = filtered_df[filtered_df['platform'] == platform_filter]
        
        # Sort
        filtered_df = filtered_df.sort_values(
            by=sort_by, 
            ascending=(sort_order == "Ascending")
        )
        
        # Display filtered and sorted data
        st.dataframe(filtered_df)

if __name__ == "__main__":
    main()