# Westworld Map

This map is part of the Westworld Deep Dive at the Bit Academy. Made with Midjourney & ChatGPT Code Interpreter.

## Generating the map tiles

### Step 1: Install `virtualenv`

First, you'll need to install the `virtualenv` package if you don't have it already. Open your terminal and run the following command:

```bash
pip3 install virtualenv
```

### Step 2: Create a Virtual Environment

Navigate to the directory where you want to create your virtual environment, and then run the following command to create a new virtual environment named `westworld_map`:

```bash
virtualenv python-environment
```

### Step 3: Activate the Virtual Environment

To activate the virtual environment, run the following command:

- **For macOS and Linux:**

  ```bash
  source python-environment/bin/activate
  ```

- **For Windows:**
  ```bash
  .\python-environment\Scripts\activate
  ```

### Step 4: Create a `requirements.txt` File

Create a file named `requirements.txt` in your project directory and add the following lines to specify the required packages:

```
Pillow==8.3.2
matplotlib==3.4.3
```

### Step 5: Install the Required Packages

With the virtual environment activated, run the following command to install the required packages from the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

### Step 6: Run the Code Snippets

Now, you can copy and paste the code snippets provided earlier into a Python script (e.g., `generate_tiles.py`) and run it using the following command:

```bash
python generate_tiles.py
```

### Step 7: Deactivate the Virtual Environment (Optional)

When you're done, you can deactivate the virtual environment by running:

```bash
deactivate
```
