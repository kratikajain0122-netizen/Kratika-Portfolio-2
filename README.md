# Kratika's Portfolio Website

This is a responsive portfolio website built with HTML, CSS, and JavaScript.

## 🚀 How to Add New Projects

The "Creative Projects" section is powered by a data file (`projects_data.js`) which is automatically generated from your folders.

### Step 1: Add Media
1.  Go to the `Carousel` folder.
2.  Create a folder for the **Brand** (e.g., `Nike`).
3.  Inside that, create a folder for the **Product/Project** (e.g., `Air Jordan Campaign`).
4.  Add your images (JPG/PNG) inside that project folder.

### Step 2: Update the Website
Since this is a static website, you need to tell it about the new files.

1.  Open your terminal.
2.  Run the generation script:
    ```bash
    python3 generate_projects_json.py
    ```
3.  This will update `projects_data.js` automatically.
4.  Reload your `index.html` to see the changes!

## 🌐 Deploying to GitHub Pages

This website is **100% compatible** with GitHub Pages.

1.  Push all your files (including the newly generated `projects_data.js`) to your GitHub repository.
2.  Go to **Settings > Pages** in your repository.
3.  Select the `main` branch as the source.
4.  Your site will be live!

**Note:** The Python script (`generate_projects_json.py`) runs **locally on your computer**. GitHub Pages will simply serve the `projects_data.js` file you generated. It will not run the Python script for you. Always run the script locally before pushing changes.
