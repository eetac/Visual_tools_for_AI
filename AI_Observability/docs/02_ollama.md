## 2. WHAT IS OLLAMA?

Ollama is an open source tool that allows you to download, manage and run LLMs directly on a computer. It is compatible with different families of models, such as Qwen, Llama or Gemma and facilitates its execution without the need to depend on external cloud services. Ollama is not an AI model per se, but rather the software that loads the models and manages the computing resources needed to run them, leveraging the computer's CPU and, when supported, GPU to speed up inference.

One of the main advantages of Ollama is that it allows you to run artificial intelligence models locally, maintaining control over the data and without costs per query. Once downloaded, the models can be used without an Internet connection to perform tasks such as generating text, answering questions, analyzing code, or processing images, depending on the capabilities of each model. In addition, Ollama provides a local API that facilitates the integration of models with Python applications, graphical interfaces and frameworks such as LangChain or LangGraph, allowing the development of customized artificial intelligence applications and agents.

## 2.1. INSTALLATION AND USE OF OLLAMA

### 2.1.1. CHECKING THE CHARACTERISTICS

Before installing Ollama you can check the processor and available memory.

| Operating system     | Command                                |
| -------------------- | -------------------------------------- |
| macOS                | `system_profiler SPHardwareDataType`   |
| Linux                | `sudo dmidecode -t system`             |
| Windows (PowerShell) | `Get-CimInstance Win32_ComputerSystem` |

From Terminal:

```bash
# MacOs
system_profiler SPHardwareDataType
```

```bash
# Linux
sudo dmidecode -t system
```

```bash
# Windows (PowerShell)
Get-CimInstance Win32_ComputerSystem
```

Information similar to:

| Feature                         | Value                                      |
| ------------------------------- | ------------------------------------------ |
| Model name                      | MacBook Pro                                |
| Model identifier                | Mac16,8                                    |
| Model number                    | MX2J3Y/A                                   |
| Chip                            | Apple M4 Pro                               |
| CPU                             | 14 cores (10 performance and 4 efficiency) |
| RAM memory 24 GB                |
| System firmware version         | 20457.1.29                                 |
| Operating System Loader Version | 20457.1.29                                 |

<p align="center">
  <sub>Figure 2. Mac information</sub>
</p>

On some Mac computers with Apple Silicon (such as M1, M2, M3, M4), Ollama can use the chip's integrated GPU to accelerate model execution.

### 2.1.2. INSTALL OLLAMA

Open the Terminal application and run:

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

This script downloads and installs Ollama on macOS and adds the ollama command to the system.

When finished, check that it has been installed correctly:

```bash
ollama --version
```

You should see a response similar to: ollama version X.X.X

To open the Ollama startup wizard:

```bash
ollama
```

### 2.1.3. CHOOSE A MODEL

Before downloading a model it is important to choose one that fits the available resources of the computer. The main factors to consider are the available memory of the MAC, the size of the model, the context to be used and the type of task.

Ollama has a library of models where you can consult the different families and versions available. This library is continuously updated with new models.

It is important to know that the same model can have different sizes. For example, qwen3.5:4b and qwen3.5:9b. Where the letter B indicates approximately the number of billions of parameters.

In general, a larger model indicates more capacity and more reasoning, but also more memory, more consumption and less speed. A bigger model is not necessarily always better. It also depends on your architecture, training and specialization.

To see the approximate size of each model, you can search in the Ollama library. For example, the Qwen 3.5 family currently has variants such as:

| Model          | Approximate size |
| -------------- | ---------------: |
| `qwen3.5:0.8b` |       1.2–1.3 GB |
| `qwen3.5:2b`   |       2.7–3.1 GB |
| `qwen3.5:4b`   |       3.3–4.0 GB |

The file size does not exactly correspond to the total memory it will consume during execution. You also need memory for context, cache, buffers, operating system... Therefore, it is not recommended to choose a model that takes up practically all the available memory.

### 2.1.4. DOWNLOAD A MODEL

Once the model is chosen, it is downloaded.

To download a model (for example: qwen3.5:9b):

```bash
#ollama pull model_name
ollama pull qwen3.5:9b
```

Progress will be shown during the download (pulling manifest, pulling …, success).

Multiple models can be installed. These models are saved to disk on the Mac. Having multiple models installed does not mean that they are all taking up RAM at the same time. Significant memory is consumed when the model is loaded and running.

### 2.1.5. CHECK INSTALLED MODELS

To check which models are installed:

```bash
ollama list
```

Example:

| NAME       | ID           | SIZE   | MODIFIED      |
| ---------- | ------------ | ------ | ------------- |
| qwen3.5:4b | 7f3251fa6878 | 4.0 GB | 5 minutes ago |
| gemma3:12b | f4031aab637d | 8.1 GB | 3 weeks ago   |
| qwen3.5:9b | 56671c2ab938 | 6.6GB  | 3 weeks ago   |

<p align="center">
  <sub>Figure 3. Installed models</sub>
</p>

### 2.1.6. RUN A MODEL

To run the model and start a conversation:

```bash
ollama run qwen3.5:9b
```

Then >>> will appear and the conversation can start.

### 2.1.7. CHECK MODELS LOADED TO MEMORY

To see which models are currently loaded and also to see if the model is suitable for our mac, in another terminal we run:

```bash
ollama ps
```

A sort of table with relevant information will appear per terminal:

| NAME       | ID           | SIZE   | PROCESSOR | CONTEXT | RUNNER   | UNTIL              |
| ---------- | ------------ | ------ | --------- | ------- | -------- | ------------------ |
| qwen3.5:9b | 56671c2ab938 | 7.9 GB | 100% CPU  | 65536   | llamacpp | 4 minutes from now |

<p align="center">
  <sub>Figure 4. ollama ps</sub>
</p>

The ideal case is 100% GPU as it indicates that the model is fully using graphics acceleration.

You can also open Activity Monitor → Memory and check the memory pressure.
If the pressure remains green and the system continues to run smoothly, the model is suitable.
If the memory pressure is yellow or red, the Mac is very slow, or the model lags excessively, use a smaller model or reduce the context.

### 2.1.8. TO STOP A MODEL

When we no longer need to ask a model any more questions, it is written: ollama stop qwen3.5:9b

With this command, we stop the model. That is, it is not removed from the disk but is unloaded from memory, stops using GPU and frees resources.

To check that it stopped correctly:

```bash
ollama ps
```

(and should come out empty)
