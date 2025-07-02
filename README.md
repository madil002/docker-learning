
# Docker learning



## What is Docker?
Docker is a powerful tool for modern development and operations. It revolutionizes the way applications are built, shipped and run by using containerization.


## What are Containers?
Containers are lightweight, portable units of running applications. They bond to an application with all its dependencies, ensuring it runs consistently across different environments. 

Containers run on the Docker Engine, which relies on the host operating system to provide a consistent runtime environment. By sharing the same kernel, containers remain lightweight and efficient. This structure sits on top of the underlying physical hardware, ensuring optimal resource usage and portability.

By isolating the application from the underlying system, containers guarantee that it runs exactly the same, whether on a developer's laptop, a testing server, or in production - solving the notorious "It works on my machine" problem, making deployment smoother and more reliable across the entire development lifecycle.

### Key benefits:
* Prevents conflicts and ensures that applications can run smoothly without interfering which each other e.g app a runs python v2.7 whilst app b runs python 3.8
* More resource efficient compared to traditional VMs
* They share the host kernal - reducing overhead and allows more containers to run on the same hardware (unlike VMs, which require a full OS instance for each one)
## Key Components of Docker
**Docker Engine** - A portable, lightweight application runtime and packaging tool. Its the core service that runs and manages containers *(Think of it as the engine of a car - its what powers the whole thing)*

**Docker Hub** - A Cloud service for sharing applications and automating workflows. You can pull official images, community contributed images, or even share your own images with others. *(Its like the App Store for Docker images)*

**Images** - Templates for creating containers. Its a snapshot of an application at a certain point in time. Images are immutable, meaning once they are created, they cannot be altered. To make changes, a new image must be built.

Containers are **running instances** of these images. *(Think of the image as a recipe and the container as the dish you create from it)*
## What are Virtual Machines?
Virtual Machines (VMs) are software emulations of physical computers. Each VM runs its own complete operating system and functions as an independent system,  allowing multiple operating systems to coexist on a single physical machine.

Each VM is fully isolated, with its own binaries, libraries, and resources. As a result, VMs are resource-intensive, requiring dedicated CPU, memory, and storage allocations.

### VMs vs Containers:
| VMs                                | Feature             | Containers                                |
|------------------------------------|---------------------|-------------------------------------------|
| **Takes minutes** – *Each VM boots a full OS* | Startup Time        | **Takes seconds** – *Containers share the host OS* |
| **Resource heavy** – *Requires significant resources for a full OS* | Resource Usage      | **Lightweight** – *Only uses necessary resources* |
| **Strong isolation** – *Each VM is fully isolated with its own OS* | Isolation           | **Process-level isolation** – *Containers share the host kernel but are isolated at the process level, offering sufficient isolation* |
| **Lower portability** – *VMs are dependent on the hypervisor and OS* | Portability         | **High portability** – *Containers are highly portable across environments due to the Docker image format* |


## Dockerfile

A Dockerfile contains a set of instructions on how to build the Docker image. It defines the environment, dependencies, and configuration needed to run an application inside a container. Each instruction in a docker file creates a layer in the image, making it easy to track changes and optimize builds.

### Common instructions:
* `FROM` - Specifies the base image to use for the docker image 
* `RUN` - Executes commands in the container at runtime 
* `COPY` - Copies files from the host machine into the container
* `WORKDIR` - Sets the working directory for subsequent commands
* `CMD` - Specifies the command to run when the container starts

### Example Dockerfile:
```dockerfile
# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Run app.py when the container launches
CMD ["python", "app.py"]
```

## Docker Networking
Docker networking controls how containers talk to each other, the host, and the outside world. Networking is important as it allows containers to communicate securely and efficiently with each other, whether they're sharing data or working together in larger applications.

Docker networking is particularly important because it simplifies the implementation of microservices architecture, allowing different parts of an application to run as independent services each in its own container ensuring that these services can communicate with each other.

### Types of Networks:

1. **Bridge** - The default network mode for containers on the same machine. Containers connected to the Bridge Network can communicate with each other using their own IP addresses. This network is isolated from the host network, providing an extra layer of security
2. **Host** - Containers use the host machines network directly without any isolation. Its as if the container is plugged directly into your home network with no distinction between the container and the host
3. **None** - The None Network gives a container no network interface at all, which makes it completely isolated. *Like a room with no doors or windows*
## Docker Compose
Docker Compose is a powerful tool for managing multi-container applications. It lets you define all your services in a single file and manage them collectively, rather than manually starting and stopping containers one by one. Docker compose acts as an organiser that web servers, databases, caching layers, and other services work together smoothly by automatically creating a network.

### Example `docker-compose.yml`:
``` yml
version: '3.8'

services:
  web:
    image: nginx:latest
    ports:
      - "80:80"
    depends_on:
      - redis

  redis:
    image: redis:latest
```
> This docker-compose.yml file sets up Nginx as a web server using the latest Nginx image, binds port 80 on the host to port 80 in the container, and ensures the web server won’t start until Redis is up and running.
>
## Multistage Builds

Multistage builds in Docker let you use multiple `FROM` statements in your Dockerfile, allowing you to build your application in one stage and create a lightweight final image in another. The first stage includes all the dependencies needed to build the application, but these are not included in the final image. This approach discards unnecessary files and dependencies, resulting in a smaller, more optimized image.

Smaller images are quicker to pull from regisries, faster to deploy and takes up less disk space.

``` dockerfile
# Stage 1: Build the app
FROM node:18 AS builder
WORKDIR /app
COPY . .
RUN npm install && npm run build

# Stage 2: Serve with Nginx
FROM nginx:latest
COPY --from=builder /app/build /usr/share/nginx/html
```

>* Stage 1: Builds the app using Node.js.
>* Stage 2: Uses Nginx to serve only the built files, keeping the final image small.

**How does this reduce size?** In the build stage, system-level dependencies installed with tools `like 1apt-get` or Python packages via `pip` are stored in directories like `/usr/bin` or `/usr/local/lib/python/site-packages`, not in the `/app` folder. Since only the built files from `/app/build` are copied to the final image, all these extra dependencies are left behind, resulting in a much smaller and more efficient image.

## Control Groups (cgroups)

Control Groups (cgroups) are a Linux kernel feature that allows you to allocate, prioritize, and limit the resources (such as CPU, memory, disk I/O, etc.) available to processes or groups of processes. Essentially, cgroups enable the management and isolation of system resources, which is crucial for containers (like Docker) to run efficiently and securely on a host machine.

#### Key features:

1. **Resource Limiting**: You can set limits on how much CPU, memory, or disk a process or container can use.
2. **Prioritization**: You can assign priority to certain processes or containers, ensuring that critical workloads get more resources.
3. **Accounting**: Track and measure resource usage for specific processes or groups of processes.
4. **Isolation**: Ensure that one process or container doesn’t interfere with the performance of others by limiting its resource access.

#### Example command:
`docker run --cpus="1.5" nginx`
> This command starts an Nginx container and limits it to 1.5 CPU cores

## Namespaces

Namespaces in Docker are a way to isolate different aspects of a container's environment, ensuring containers run independently from each other and the host system. Here are the main types of namespaces in Docker:

* **PID**: Isolates process IDs, so containers can't see or affect each other's processes.
* **NET**: Gives each container its own network stack, so they don't share network settings.
* **MNT**: Isolates filesystems, so each container has its own view of the file system.
* **UTS**: Isolates hostnames, so containers can have unique hostnames.
* **IPC**: Isolates inter-process communication (like message queues and shared memory).
* **USER**: Allows containers to map user IDs to the host, improving security.
* **CGROUP**: Isolates resource management settings (like CPU and memory) to prevent containers from affecting each other.

## Common Docker Commands


| Command                               | Description                                              |
|----------------------------------------|----------------------------------------------------------|
| `docker build .`                       | Builds an image from a Dockerfile in the current directory. |
| `docker pull <image>`                  | Downloads an image from a Docker registry (e.g., Docker Hub). |
| `docker run <image>`                   | Runs a container from the specified image.               |
| `docker ps`                            | Lists all running containers.                           |
| `docker ps -a`                         | Lists all containers, including stopped ones.            |
| `docker stop <container>`              | Stops a running container.                              |
| `docker rm <container>`                | Removes a stopped container.                            |
| `docker rmi <image>`                   | Deletes an image from the local system.                  |
| `docker exec -it <container> bash`     | Opens an interactive terminal inside a running container. |
| `docker-compose up`                    | Starts services defined in a `docker-compose.yml` file.  |
| `docker-compose down`                  | Stops and removes containers started by Docker Compose.  |

## Additional Resources
* **[Official Docker Documentation](https://docs.docker.com/)**
* **[Docker Hub](https://hub.docker.com/)**