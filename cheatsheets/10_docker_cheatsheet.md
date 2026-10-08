# Commands

- `docker system df` - show disk space usage
- `docker system prune` - delete unused data
- `docker run <registry (user)>/<repository (name)>:<tag>` - run a container based on an image
- `docker run [-i] [-t] [-d] [--rm] [--name <container_name>] [-v <volume_name_or_local_path>:<where_to_mount_inside_container_filesystem] [--network <network_name>] [--network-alias <alias>] [-p <host_port>:<container_port>] <image, e.g. ubuntu:latest>` - run a container based on an image
  - `-i` and `-t` add a pseudo, interactive terminal, this terminal has the possibility to take input (`-i`) and behaves like a real terminal (`-t`)
  - `-d` allows the container to run in the background
  - `--rm` means that the container and its anonymous volumes will be deleted after the container exits
  - `--name` specifies name of the container
  - `-v` mounts (maps) a volume or a host's filesystem path to a virtual path visible inside the container
    - for volume mounts the option with `-v` could be for example `-v my-volume:/my-container-dir`
    - for bind mounts the option with `-v` could be for example `-v ${PWD}/mylocaldir:/my-containerdir`
      - `PWD` means "Present Working Directory"
  - `--network` attaches the container to a network
  - `--network-alias` creates an alias (a DNS name) for the container to present itself using this alias in the specified network, e.g. instead of `docker.internal.host:5432` you can write `postgres:5432`
  - `-p` associates the specified container's port with the specified host's port
- `docker image ls -a` - list all images
  - note that an image can have more than one tag, if one image is referenced by more than one tag, all those tags will be displayed, creating an illusion as if there were more than one image, in such case you need to look at IDs (digests) and compare them to see if different tags actually correspond to the same image or to different images
- `docker container ls -a` - list all containers
- `docker container kill <container_id>` - kill a specified container
  - can be used for example to test how Docker Swarm replaces the killed containers with new ones to satisfy the desired number of replicas for the given service
- `docker start <container_name>` - start the specified stopped container
- `docker stop <container_name>` - stop the specified running container
- `docker attach <container_name>` - attach STDIN, STDOUT and STDERR to the given container, in practice it opens the container's pseudo terminal
- `docker build -t <image_name> [-f <dockerfile_name>] [--target=<stage_name>] [--secret id=<build_time_secret_id>,src=<local_path_to_secret>] [--pull] [--no-cache] <directory with Dockerfile inside, or some other build context>` - perform building, i.e. create an image from a Dockerfile and a set of project files known as the build context
  - `--pull` forces Docker to check for and download a newer version of the base image even if there is already a version cached locally, this can be useful because a specific image tag can change the digest it points to over time as the developers update their images with patches, fixes, etc.
  - `--no-cache` disables the build cache and forces Docker to rebuild the image layer by layer from scratch, this allows to get fresh dependencies but not fresh base images
- `docker volume create <volume_name>` - create a new volume for storing persisting data
- `docker login` - login
  - required before pushing an image to a registry
- `docker tag <source_img> <target_img>` - add a new tag (`<target_img>`) to the source image (`source_img`)
  - useful for adding the correct tag corresponding to the repo where we want to push the given image, in such case `<target_img>` should be `<username>/<repo_name>:<my_tag>`
- `docker push <username>/<repo_name>:<my_tag>` - push the specified image to the specified repo
- `docker pull <username>/<repo_name>:<my_tag>` - pull the specified image from the specified repo
- `docker network ls` list networks
- `docker network (create | rm) <name>` - create/remove a network
- `docker ps` - list containers
- `docker logs <container_id>` - show logs of the container
- `docker compose build` - use the compose yaml file to build all necessary images
- `docker compose up [-d]` - use the compose yaml file to create and run containers
  - `-d` runs them in the background
- `docker compose stop` - use the compose yaml file to stop the containers running in the background
- `docker compose -f <yml_file_1> -f <yml_file_2> ...` - use/overlay more than one file in the compose command
  - the options in the next file in the sequence will override and/or merge with the options in the previous file
- `docker swarm init` - initialize a swarm on the current device
  - turns the current device into a manager node
- `docker swarm leave [--force]` - leave the swarm
  - turns-off the swarm mode on the current machine
- `docker stack deploy -c <stack_yml_file> [--with-registry-auth] <stack_name>` - start or update a stack defined by the yaml file
  - `--with-registry-auth` is an additional authentication flag in case Docker Swarm cannot find/access your images on your Docker Hub repo
  - also, make sure to be logged in to Docker before deploying a stack
- `docker stack services <stack_name>` - view active services and replica count in the given stack
- `docker stack rm <stack_name>` - remove the stack along with all its containers, networks, services, tasks, etc.
- `docker service ps <stack_name>_<service_name>` - view exact container tasks running across nodes
- `docker service logs <stack_name>_<service_name>` - view logs of the given service
- `docker service scale <stack_name>_<service_name>=<how_many_replicas>` - manage the number of replicas of a given service
- `docker secret create <secret_name> <file_name>` - create a swarm secret based on the contents of the file
  - if the file is not provided, you can use pipes and `-` instead of a file to provide secret content to the command, e.g. `echo "my_secret" | docker secret create my_swarm_secret -`
- `docker exec <container_id> <command>` - execute a command in a running container

# 3 most important Docker ideas

> [!TIP]
> **Enveloping/Containerization**
> 
> Instead of telling someone
> * *"Install Python version X.YZ, these libraries, set up this configuration like this, ..., and then run the application"*,
> 
> you tell someone
> * *"Just run this Docker image and it will automatically create a running container containing the entire application and everything this application needs"*,
> 
> and the important point is that those multiple dependencies, e.g. Python version, etc., are already packaged/enveloped inside the image so you don't have to worry about them anymore.

> [!TIP]
> **Isolation**
> 
> Isolated, independent processes make the entire operating system more manageable and modular.

> [!TIP]
> **Cache, Sharing, Extending, Generality**
> 
> Programs should be lightweight and cacheable, easy to distribute and share, easy to extend and to use as building blocks inside other programs, and possible to run the same everywhere on every machine.

# Introduction

A program is not just a textfile. A program is a process + a bunch of things that the process depends on.

For example:

```
Python process
    │
    ├── Python interpreter
    ├── Python packages
    ├── your source code
    ├── configuration files
    ├── environment variables
    ├── filesystem
    ├── network
    └── CPU / RAM
```

Dependencies are provided by the operating system and the machine.

The fundamental problem Docker addresses is: ***"How can I give you not just my application, but the environment it expects to run in?"***

But there's an important complication. You don't want to give someone an entire computer. You don't want: *"Here's a complete operating system. Please install it and run my application."* You want something much smaller: *"Here's the environment my process needs. Run my process inside it."*

Docker solves this classic ***"it works on my machine but not on yours"*** problem by packaging (enveloping) applications into standardized units that run identically everywhere and contain everything needed to run an application.

> [!WARNING]
> Docker does not make software universally executable on all machines. It simply moves this problem to a different scope.

Imagine that without Docker you have:

```text
Application
   ↓
Python 3.12
   ↓
Python libraries
   ↓
System libraries
   ↓
Operating system
   ↓
Hardware
```

Your colleague might have:

```text
Application
   ↓
Python 3.11       ← different!
   ↓
Different libraries
   ↓
Different system libraries
   ↓
Different operating system
   ↓
Different hardware
```

So your application may work on your device but it may not work on your colleague's.

With Docker, you package the application together with its **userspace environment**:

```text
┌──────────────────────────┐
│       Docker image       │
│                          │
│  Application             │
│  Python 3.12             │
│  Python libraries        │
│  System libraries        │
│  Configuration           │
└──────────────────────────┘
             ↓
Docker runtime (running Docker container)
             ↓
Host operating system + kernel
```

Now everyone can run essentially the same image.

**So instead of saying:**

> ***"Install Python 3.12, these 17 libraries, these system packages, configure them this way..."***

**you can say:**

> ***"Run this Docker image."***

For example, it doesn't matter what Python you have installed on your operating system because your dockerized application doesn't use the host's Python installation. It uses the Python packaged in the image and running inside the container. The host operating system still matters for providing actual physical resources, but the application environment becomes much more controlled and reproducible and more easily distribuable across different machines.

---

But **Docker itself must exist**

Docker solves:

> *"Does the application have the same environment?"*

It does not solve:

> *"Can the computer run Docker?"*

You still need a compatible Docker/container runtime.

A useful mental model is:

> **Docker standardizes the userspace, not the entire computer.**

For example, a Docker image can specify:

```text
Ubuntu userspace
Python 3.12
numpy 2.x
your application
configuration
...
```

But it doesn't normally contain its own Linux kernel.

The kernel comes from Linux host or (on Windows/macOS) from Linux VM. This is also why Docker containers are generally much lighter than full virtual machines.

Moreover, Docker packages applications such that they are completely **isolated** from each other and from the operating system, as if they were running within their own virtual operating systems.

# History (bare metal -> virtual machines -> containers)

## 1. Bare metal 🖥️

### Idea

You have **one physical computer** and install an operating system directly on it.

```text
┌──────────────────────────┐
│ Application              │
├──────────────────────────┤
│ Operating System         │
├──────────────────────────┤
│ Physical Hardware        │
└──────────────────────────┘
```

### Problem

Suppose you have:

```text
Server
 ├── App A → needs Python 3.10
 ├── App B → needs Python 3.12
 └── App C → needs a different version of some library
```

They all use the same OS environment.

**This can lead to:**

* **dependency conflicts**
* **difficult setup**
* **applications interfering with each other**
* **poor utilization of the server**

You could buy another physical machine, but that's expensive and inefficient.

## 2. Virtual Machines 💻

The next idea:

> **Pretend that one physical computer is actually several computers.**

A hypervisor creates virtual machines.

```text
┌────────────────────────────────────────┐
│            Physical Machine            │
│                                        │
│ ┌──────────────┐      ┌──────────────┐ │
│ │     VM #1    │      │     VM #2    │ │
│ │              │      │              │ │
│ │ Application  │      │ Application  │ │
│ │              │      │              │ │
│ │ Guest OS     │      │ Guest OS     │ │
│ └──────────────┘      └──────────────┘ │
│                                        │
│               Hypervisor               │
│                                        │
│           Physical Hardware            │
└────────────────────────────────────────┘
```

For example:

```text
Physical server
       │
       ▼
   Hypervisor
    /     \
   /       \
 VM #1     VM #2
 Linux     Linux
 App A     App B
```

Each VM behaves approximately like a separate computer.

You can have:

```text
VM #1 → Ubuntu + App A
VM #2 → Windows + App B
VM #3 → Ubuntu + App C
```

Each VM can have its own:

* operating system
* libraries
* applications
* filesystem
* virtual CPU
* virtual RAM
* virtual network interface

**Virtual Machine = virtual computer**, i.e. software-created computer.

The hypervisor gives each VM **virtual hardware**, i.e. it **schedules (maps) virtual hardware to physical hardware over time**.

## 3. Hypervisor

The **hypervisor is the software responsible for managing VMs**.

Think of it as a **traffic controller between VMs and the physical hardware**.

```text
  VM #1       VM #2
    │           │
    ▼           ▼
┌────────────────────┐
│     Hypervisor     │
└────────────────────┘
          │
          ▼
Physical CPU / RAM / Disk
```

It decides things like:

* *"VM #1 gets some CPU time."*

* *"VM #2 can use this amount of RAM."*

* *"This VM's virtual disk corresponds to this part of the physical storage."*

## 4. Why VMs are relatively heavy

Remember:

> **A VM contains an entire operating system.**

For example:

```text
VM #1
├── Application
├── Libraries
├── Ubuntu
│   ├── kernel
│   ├── system services
│   └── other OS components
└── Virtual hardware
```

```text
VM #2
├── Application
├── Libraries
├── Ubuntu
│   ├── another kernel
│   ├── system services
│   └── other OS components
└── Virtual hardware
```

**So you're effectively running several computers inside one computer.**

This provides **strong isolation**, but there's **considerable overhead**.

## 5. Containers 📦

Containers take a different approach.

Instead of pretending to have several complete computers:

> **Run several isolated applications on the same operating system.**

Conceptually:

```text
┌───────────────────────────────────────┐
│              Host Machine             │
│                                       │
│ ┌─────────────┐    ┌─────────────┐    │
│ │ Container 1 │    │ Container 2 │    │
│ │             │    │             │    │
│ │ Application │    │ Application │    │
│ │ Libraries   │    │ Libraries   │    │
│ └─────────────┘    └─────────────┘    │
│                                       │
│          Container Runtime            │
│                                       │
│          Operating System             │
│                                       │
│          Physical Hardware            │
└───────────────────────────────────────┘
```

The important difference:

### VM

```text
Application
Libraries
Guest OS
Virtual Hardware
```

### Container

```text
Application
Libraries
────────────
Shared Host OS
────────────
Hardware
```

Containers **do not normally contain their own operating-system kernel**.

## 6. What does a container actually contain?

A useful mental model is:

> **A container packages an application together with the things the application needs from the user space.**

For example:

```text
Python application
      +
Python interpreter
      +
Python libraries
      +
configuration
      +
other dependencies
      ↓
  Container
```

So instead of telling someone:

> *"Install Python 3.12, then install these 17 packages, then configure these environment variables..."*

you can give them a container image:

```text
my-python-app
```

and the environment can be created consistently.

## 7. Container vs VM — the most important distinction


|                  | Virtual Machine  | Container                        |
| ---------------- | ---------------- | -------------------------------- |
| **What is it?**      | Virtual computer | Isolated application environment |
| **Own OS?**          | Yes              | No, no separate kernel               |
| **Own kernel?**      | Yes              | No, shares host kernel               |
| **Overhead**         | Generally larger | Generally smaller                |
| **Startup**          | Generally slower | Generally faster                 |
| **Isolation**        | Strong           | Strong, but different mechanism  |
| **Main abstraction** | Machine          | Application/process              |

## 8. Intuitive analogy 🏢

Imagine an apartment building.

### Bare metal

You own an entire house:

```text
🏠 One physical machine
└── One OS
    └── Applications
```

### Virtual machines

You turn the building into several independent houses:

```text
🏠 VM #1 → complete house
🏠 VM #2 → complete house
🏠 VM #3 → complete house
```

Each has its own kitchen, bathroom, etc.

### Containers

Instead, you have apartments:

```text
🏢 Building
├── Apartment 1 → App A
├── Apartment 2 → App B
└── Apartment 3 → App C
```

They have their own spaces and are isolated, but they share some infrastructure.

The analogy isn't perfect technically, but it's useful for remembering the main distinction:

> **VMs virtualize machines; containers isolate applications/processes.**

# Docker 🐳

**Docker is a platform/tooling ecosystem for building, distributing, and running containers from images.**

A simplified view:

```text
Dockerfile
    ↓
docker build
    ↓
Docker Image
    ↓
docker run
    ↓
Docker Container
```

> [!TIP]
> Think:
> * **Dockerfile = textfile defing an image**
>   * analogy: my_class.py
> * **Image = blueprint**
>   * analogy: class
> * **Container = running instance of that image**
>   * analogy: instance of a class

> [!TIP]
> Other useful terms:
> 
> * **Registry (e.g., Docker Hub):** A centralized repository for storing and sharing images. You *pull* pre-built images (like Node.js, PostgreSQL, or Nginx) from a registry and *push* your custom images to it.
> * **Docker Compose:** A tool that uses a YAML configuration file (`docker-compose.yml`) to define and run multi-container applications (e.g., spinning up a web app, a Redis cache, and a Postgres database simultaneously with one command).

## Dockerfile

It is a file that defines step by step how to build (create) an image and what should happen at start when a container is created based on that image and starts running.

## Image

An image is essentially a packaged template for creating containers. It can be shared so that others can download it and use it or extend it by including it in other images.

For example, an image:

```text
my-app:1.0
```

can describe:

```text
Python
+ dependencies
+ application code
+ configuration
```

## Container

A container is a running, independent instance created from an image.

```text
Image
  │
  ├── Container #1
  ├── Container #2
  └── Container #3
```

The **container runtime** is the software responsible for actually creating and running containers.

Imagine you have:

```text
100 applications
```

You don't necessarily want:

```text
100 virtual machines
```

because each VM needs an operating system.

With containers:

```text
One operating system
│
├── Container → App 1
├── Container → App 2
├── Container → App 3
├── Container → App 4
├── ...
└── Container → App 100
```

The containers can be much more lightweight. This makes it practical to run many isolated application workloads on the same machine.

# Kubernetes ☸️

Suppose you have one server:

```text
Server
├── Container A
├── Container B
└── Container C
```

Docker can help you run these. **But what if your system grows?**

```text
Server #1
├── 20 containers

Server #2
├── 30 containers

Server #3
├── 25 containers

Server #4
├── 40 containers
```

Now you have a new problem: who manages all the containers?

For example:

* What happens if a server crashes?
* How do we replace a failed container?
* How do containers communicate?
* How do we distribute traffic?

This leads to **orchestration**.

> **Orchestration = Automatically managing lots of containers across machines.**

Think of an orchestra 🎻. You don't want to manually tell every musician:

> "Play now. Stop. Start again. You're too loud. You broke, replace yourself."

You have a conductor coordinating everything.

**Kubernetes is a container orchestration system.**

Its job is broadly:

> **Keep a cluster of machines and containerized applications in the desired state.**

For example, you tell Kubernetes:

```text
"I want 5 instances of my web application."
```

Kubernetes can manage:

```text
Server 1
├── App
├── App

Server 2
├── App
├── App

Server 3
└── App
```

If one container dies, Kubernetes can detect that the desired state isn't satisfied and arrange for replacement workloads to run elsewhere, assuming the cluster has the necessary capacity.

# Real world example

```text
Physical Machine
│
├── Hypervisor
│
├── VM #1
│   ├── OS
│   └── Container Runtime
│       ├── Container #1
│       └── Container #2
│
└── VM #2
    ├── OS
    └── Container Runtime
        ├── Container #3
        └── Container #4
```

This is a **very common real-world setup**.

The containers are running inside VMs.

That might initially seem contradictory:

> "I thought containers replaced VMs?"

They don't necessarily replace them.

They solve **different problems** and can be used together. For example, cloud infrastructure may use VMs to provide isolation between customers, while applications inside those VMs are deployed as containers.

# Low level details

Suppose you have:

```text
myapp/
├── app.py
└── requirements.txt
```

`app.py`:

```python
import requests

print(requests.get("https://example.com").status_code)
```

On your computer you might do:

```bash
python app.py
```

At a low level, roughly this happens:

```text
you
 │
 │ execute
 ▼
python
 │
 ├── loads Python interpreter
 ├── loads app.py
 ├── loads requests
 ├── loads other Python packages
 ├── opens files
 ├── creates network connections
 └── becomes a running process
```

**Docker container is basically the same thing: a normal Linux process. The difference is that Docker configures Linux so that this process has a restricted/isolated view of the system.**

For example, normal process:

```text
        Linux
┌─────────────────────────────┐
│                             │
│ /home/kamil                 │
│ /etc                        │
│ /usr                        │
│ other processes             │
│ network interfaces          │
│ etc.                        │
│                             │
└─────────────────────────────┘
              ▲
              │
           process
```

A containerized process might see something more like:

```text
        Linux
┌─────────────────────────────┐
│                             │
│  Container's filesystem     │
│  Container's processes      │
│  Container's network        │
│                             │
│       Python process        │
│                             │
└─────────────────────────────┘
```

**It feels like a separate machine, but underneath it is still using the host's Linux kernel.**

But how can a normal process "think" it's alone?

It's thanks to the following 3 concepts:

* **namespaces**
* **cgroups**
* **layered filesystem**

> [!NOTE]
> A **partition** in Linux is a distinct section of a physical hard drive or solid-state drive that acts as an independent storage unit.

> [!NOTE]
> A **network share** in Linux is a folder or directory hosted on one computer that other devices on the same network can access, read, and write to as if the files were on their own local hard drive.

> [!NOTE]
> A **mount point** in Linux is a directory in the file system tree where an external storage device, partition, or network share is attached to make its files accessible.

## Namespaces

> **What the container can SEE?**

> ***"When this process asks Linux what exists, show it this particular view."***

> **Namespace = A restricted/isolate-able view of some Linux resources.**


3 most important namespaces:

* processes
* networking
* mount points

### Processes

Normally Linux has one global process list:

```
PID 1    systemd
PID 100  firefox
PID 200  python
PID 300  docker...
```

A process inside a container can instead have its own PID namespace.

Inside the container:

```
PID 1    python
PID 2    something else
```

Meanwhile the host might see:

```
PID 18432    python
```

So:

```
HOST VIEW:
PID 18432 → Python


CONTAINER VIEW:
PID 1 → Python
```

**It's the same underlying process, but different views of process IDs.**

This is one of the things that makes a container look like a small independent environment.

### Networking

The same idea applies to networking, where a Python program might think: *"I have my own networking interface"*, while in reality this is just a **mapping between host's IP+port and container's IP'+port'**.

So your Python application can believe:

> *"I have my own network interface."*

It doesn't literally have a physical network card. Linux is providing an isolated network view.

### Mount points

Again, the same idea goes for mount points.

Your normal machine might have:

```
/
├── bin
├── home
│   └── kamil
├── usr
├── etc
├── var
└── ...
```

Your container might see:

```
/
├── bin
├── app
│   ├── app.py
│   └── requirements.txt
├── usr
├── etc
└── ...
```

**The container doesn't necessarily have access to the host's filesystem tree.**

Suppose your application needs:

```
Python 3.12
requests
your code
configuration
```

Docker needs some way to package those files. Imagine it creating a directory:

```
container-root/
├── usr/
│   ├── bin/
│   │   └── python
│   └── lib/
│       └── python3.12/
│           └── ...
├── app/
│   ├── app.py
│   └── requirements.txt
└── etc/
    └── ...
```

**Then Linux can start your containerized process with this directory as its root filesystem.**

From inside the process:

```
/
```

means:

```
container-root/
```

rather than:

```
the host's /
```

More details about the container's filesystem can be found in the section about layered filesystem.

### Summary

Linux Namespaces restrict what a process can view. By creating isolated namespaces for a container, the host OS limits its visibility:

* **PID (Process IDs):** The container thinks it's running as Process ID 1 on a brand-new machine, blind to all other background tasks on your computer.
* **NET (Networking):** The container gets its own virtual network interface, IP address, and routing table.
* **MNT (Mount Points):** The container only sees its own filesystem folder, completely hidden from your personal host directories.

Why not just use those manually? You actually can. Linux provides the underlying mechanisms. But imagine manually deploying your Python application. You'd need to:

1. construct a filesystem
2. install Python
3. install dependencies
4. create namespaces
5. configure networking
6. configure cgroups
7. configure mounts
8. start the process
9. manage its lifecycle
10. package/distribute everything

That's a lot. Docker gives you: `docker build` and `docker run` instead of manually assembling all of this.

## cgroups

Namespaces answer:

> *"What can the process see?"*

But we also need:

> ***"How much can the process use?"***

> **`cgroups` = A mechanism for controlling how many resources a group of processes can consume.**

Suppose your Python application has a bug:

```python
data = []

while True:
    data.append("something")
```

Eventually it consumes enormous amounts of RAM.

Without resource controls, it might hurt other processes on the machine.

Docker can use Linux **`cgroups`** (**control groups**) to **limit resources**.

For example you can set the maximum allowed RAM usage. If the container tries to consume more than it is allowed to, Linux's resource-control mechanisms can intervene. You can similarly limit CPU usage, number of processes, Disk I/O, etc.

## Layered filesystem

A **filesystem** is what allows to organize files and directories on a disk in an operating system:

```text
/
├── home/
│   └── kamil/
│       ├── notes.txt
│       └── photo.jpg
├── etc/
├── usr/
└── var/
```

Normally, when you change a file:

```text
notes.txt
```

the filesystem changes the actual file stored on disk.

That's the normal model.

Imagine instead that your filesystem is made of **transparent sheets stacked on top of each other**.

For example:

```text
Layer 1
┌─────────────────────┐
│ A.txt               │
│ B.txt               │
└─────────────────────┘

Layer 2
┌─────────────────────┐
│ C.txt               │
│ B.txt (modified)    │
└─────────────────────┘

Layer 3
┌─────────────────────┐
│ D.txt               │
└─────────────────────┘
```

When you look at the filesystem, you see:

```text
A.txt
B.txt (modified)       ← from Layer 2
C.txt
D.txt
```

> [!IMPORTANT]
> **Higher layers can hide or replace things in lower layers.**

So `B.txt` exists in Layer 1, but Layer 2 contains a newer version, so you see the Layer 2 version.

That's the basic idea.

Here's a practical example.

Suppose you have a computer with:

```text
Ubuntu
Python
Git
Node.js
...
```

And you want to create 100 environments that all start with exactly the same software.

Without layers, you might imagine:

```text
Environment 1 → 5 GB
Environment 2 → 5 GB
Environment 3 → 5 GB
...
Environment 100 → 5 GB

Total → 500 GB
```

But most of those environments contain exactly the same files.

That's wasteful.

With layers, you can have:

```text
             Shared
          ┌───────────┐
          │ Ubuntu    │
          │ Python    │
          │ Libraries │
          └───────────┘
               ↑
       shared by everyone
       /    /    \    \
      /    /      \    \
     ↓    ↓        ↓    ↓
    C1   C2       C3   C4
   changes changes changes
```

**The common data exists once.**

**Each environment only needs to store the differences.**

This layered filesystem is one of the key ideas behind Docker images and containers.

It answers:

> ***"What files can the container see and how are they managed?"***


Imagine you have three applications:

```text
app A → Python 3.12
app B → Python 3.12
app C → Python 3.12
```

You could store three complete copies:

```text
Image A
└── Python + libraries + A

Image B
└── Python + libraries + B

Image C
└── Python + libraries + C
```

**That wastes space.**

**Instead, Docker can store common filesystem pieces separately.**

For example:

```text
Layer 1
Ubuntu filesystem
```

Then:

```text
Layer 2
Python
```

Then:

```text
Layer 3
Python packages
```

Then:

```text
Layer 4
your application
```

Conceptually:

```text
┌──────────────────────────┐
│ Layer 4                  │
│ your app.py              │
├──────────────────────────┤
│ Layer 3                  │
│ requests, Flask, etc.    │
├──────────────────────────┤
│ Layer 2                  │
│ Python                   │
├──────────────────────────┤
│ Layer 1                  │
│ base filesystem          │
└──────────────────────────┘
```

The resulting filesystem appears as **one normal filesystem** to the container.

Your application doesn't see:

```text
"Ah, this file came from layer 3."
```

It simply sees:

```text
/app/app.py
/usr/bin/python
/usr/lib/...
```

> [!IMPORTANT]
> **Layers are just sets of files.**
> 
> **They are defined in the correct order in the Dockerfile and they are one of the primary components of images.**
> 
> **Containers created based on those images use those layers to define their own independent filesystems.**

Now, suppose you build:

```text
Image A
```

with:

```text
base
+
Python
+
requests
+
app A
```

Then build:

```text
Image B
```

with:

```text
base
+
Python
+
requests
+
app B
```

Docker can reuse:

```text
base
Python
requests
```

and only add:

```text
app B
```

So storage looks conceptually like:

```text
                         ┌── app A
                         │
base ─ Python ─ requests ─
                         │
                         └── app B
```

This is one reason Docker images are practical to distribute.

**If you already have the common layers, you don't need to download them again.**

Another reason why layers make it easy to share and distribute containerized applications is that **the layers defined in the images are read-only**, i.e. the files defined in them cannot be changed/modified.

The applications running inside containers, however, often have to be able to not only read data, but also write data, change it, modify, etc. This is why when a container starts running, **Docker assigns a new, temporary writable (read/write) layer on top of all read-only layers** defined in the image. This layer is created when the container is created and deleted when the container is deleted.

> [!NOTE]
> Each layer is a separate directory on the host system. They are stacked on top of each other to create a unified view when a container starts running. A new writable layer is also created specifically for each running container in the form of a new, temporary directory stored on the host system.

The important thing is that the writable layer cannot actually modify files. So how can it be writable? The idea is that all layers (read-only layers + writable layer) store **changes (deltas)** of files. For the read-only layers these deltas are persisting, while for the writable layer these changes are only temporary. All deltas are applied from the bottom-most layer to the top-most layer, giving the final, unified view of the filesystem to the running container. In the writable layer deltas are created at runtime and then get immediately destroyed when the container stops running, thus always preserving the original state of all read-only layers.

The deltas to files are applied to all layers, from the bottom layer, to the top layer (the writable layer).

```
Overlay (final view of the containerized app)
┌────────────────────────────────────────────────────────────────────┐
│   ┌─────────┐   ┌─────────┐   ┌─────────┐                          │
│   │ File-1  │   │ File-2b │   │ File-3  │                          │
│   └─────────┘   └─────────┘   └─────────┘                          │
│       │                                                            │
└───────┼────────────────────────────────────────────────────────────┘   
        │
Upper layer (N+1) (delta)
┌───────┼───────────────────────────────────────────────────────────┐
│       │         ┌─────────┐   ┌─────────┐     ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ │
│       │         │ File-2b │   │ File-3  │     ▒ File-4 whiteout ▒ │
│       │         └─────────┘   └─────────┘     ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ │
└───────┼───────────────────────────────────────────────────────────┘
        │
Lower layer (N) (original)
┌───────┼────────────────────────────────────────────────────────────┐
│   ┌─────────┐   ┌─────────┐                       ┌─────────┐      │
│   │ File-1  │   │ File-2a │                       │ File-4  │      │
│   └─────────┘   └─────────┘                       └─────────┘      │
└────────────────────────────────────────────────────────────────────┘
```

When a container starts running, runtime presents the resulting layers, with all deltas applied, as a unified filesystem:

```text
              container sees
                   /
        ┌─────────────────────┐
        │ /usr/bin/python     │
        │ /usr/lib/...        │
        │ /usr/local/...      │
        │ /app/app.py         │
        └─────────────────────┘
                  ▲
                  │
        ┌─────────┴───────────┐
        │ writable layer      │
        ├─────────────────────┤
        │ Layer C (read-only) │
        ├─────────────────────┤
        │ Layer B (read-only) │
        ├─────────────────────┤
        │ Layer A (read-only) │
        └─────────────────────┘
```

Suppose the image contains:

```text
/app/config.txt
```

and your running application does:

```python
open("/app/config.txt", "w")
```

The original image layer isn't modified.

Instead, the container gets a writable layer above the read-only image layers.

The application sees:

```text
/app/config.txt
```

as modified.

But Docker is keeping the original image unchanged and recording the container's changes separately.

Similarly with creating new files: `new.txt` exists only in the container's writable layer. As for deleting files: the deleted file is masked (whiteouted) in the writable layer.

Each container has its own writable layer and this is why an image can be reused to create many containers:

```text
                 image
                   │
          ┌────────┼────────┐
          ▼        ▼        ▼
      container  container  container
          │        │        │
       changes   changes   changes
```

All three can share the same underlying read-only image data.

> [!IMPORTANT]
> **Layers are included in the images.**
>
> **Images can be shared so that others can use images and extend them by including them in other images.**
>
> **Common images (common layers) can be reused without redownloading them.**
>
> **Each container created based on an image gets read-only layers from the image + a temporary writable layer on top of read-only layers.**
>
> **Changes (deltas) between consecutive layers define the resulting filesystem visible to the container.**
>
> **Layers can be seen as filesystem changes/deltas.**

The fact that writable layer is temporary and that read-only layers persist when container dies means that data stored inside the container's writable layer is inherently **ephemeral**, i.e. **data saved or generated when a container is running will be deleted when the container dies**.

This is why a common Docker philosophy is:

> **Containers are often disposable; important data should live outside the container.**

For example, databases shouldn't normally rely on the container's writable layer for their important persistent data. On the other hand, writable layer is useful for storing data such as temporary files or logs.

To store persistent data inside a container a common solution is to use **volumes** and **mounts**.

**If some data should be present every time an image is run (e.g. a dependency), it should be built into the image itself.**

**If data is generated on the fly (e.g. user-generated database data) and needs to persist, you can use:**

1. **Volume Mount** (also simply called **Volumes**) - path inside the Docker environment (`/var/lib/docker/volumes`), its lifecycle is managed separately by the Docker and can be used to store data that should persist even when containers are removed
   * recommended
2. **Bind Mount** - path inside host's local filesystem, connects Docker virtual environment to the real path on our system (e.g. our directory in Windows), it crosses the boundary between Docker and host (less isolation)
   * less recommended

**Modifying the layered contents of a container at runtime is not something you would normally do as this is normally done in Dockerfiles.**

> [!TIP]
> For anything we need in the container at runtime we should build it into the image! The one exception to this rule is environment specific configuration (environment variables, config files, etc...) which can be provided at runtime as a part of the environment.

> [!TIP]
> Volumes and mounts allow us to specify a location where data should persist beyond the lifecycle of a single container. The data can live in a location managed by Docker (**volume mount**), a location in your host filesystem (**bind mount**), or in memory (**tmpfs mount**).

> [!TIP]
> This third option (**tmpfs mount**) (for example: `/run/secrets/`) does not persist the data after the container exits, and is instead used as a temporary store for data you specifically DON'T want to persist (for example credential files). It is included here for completeness but should not be used for application data you want to persist.

# Low level definitions

## Dockerfile

> [!IMPORTANT]
> **A recipe for constructing the layered filesystem and defining how to start the resulting process**.

For example:

```dockerfile
FROM python:3.12

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY app.py .

CMD ["python", "app.py"]
```

Let's translate each instruction into low-level-ish operations.

---

#### `FROM`

```dockerfile
FROM python:3.12
```

Means roughly:

> **Start with an existing filesystem/image that already contains Python 3.12.**

Instead of manually creating:

```text
/usr/bin/python
/usr/lib/python...
...
```

you reuse someone else's image.

---

#### `WORKDIR`

```dockerfile
WORKDIR /app
```

Means roughly:

> **Set `/app` as the working directory for subsequent commands and the container process.**

---

#### `COPY`

```dockerfile
COPY app.py .
```

Means:

> **Put this file into the image filesystem (into the working directory of the isolated filesystem).**

Conceptually:

```text
host: myproject/app.py
       │
       │ COPY
       ▼
image: /app/app.py
```

---

#### `RUN`

```dockerfile
RUN pip install -r requirements.txt
```

This one is particularly important.

Docker temporarily starts a build environment based on the current filesystem and executes:

```bash
pip install -r requirements.txt
```

Whatever filesystem changes happen become part of a new image layer.

So conceptually:

```text
before:
/usr/...
/app/requirements.txt


now:
RUN pip install ...


after:
/usr/...
/usr/local/lib/python.../requests
/usr/local/lib/python.../...
/app/requirements.txt
```

**The resulting difference becomes another layer.**

---

#### `CMD`

```dockerfile
CMD ["python", "app.py"]
```

This is not primarily about building the filesystem.

It says:

> **When someone starts a container from this image, the default process should be `python app.py`.**

So:

```text
docker run myimage
       │
       ▼
python app.py
```

---

To summarize Dockerfile:

> **"It basically builds a stack of filesystem changes."**

Common layers of this stack can be reused.
 This is called **build caching**.

And this is one of the reasons Dockerfiles are often structured like:

```dockerfile
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
```

rather than:

```dockerfile
COPY . .
RUN pip install -r requirements.txt
```

Because changing your source code doesn't necessarily change `requirements.txt`.


## Image

> [!IMPORTANT]
> **Image = packaged (mostly read-only) filesystem made-up of layers representing filesystem changes + instructions/metadata for running a process (startup configuration).**

For example, imagine that an image contains:

```text
/
├── usr/
│   ├── bin/
│   │   └── python
│   └── lib/
│       └── python3.12/
│           ├── ...
│           └── requests/
│
├── app/
│   ├── app.py
│   └── requirements.txt
│
└── etc/
    └── ...
```

and some terminal instructions to run, like `install sth`, `run python sth`.

## Container

> [!IMPORTANT]
> **Container = a process using Linux resources = isolated views of system resources + resource limits + a specially constructed filesystem based on an image = image read-only layers plus writable layer unified/seen as one filesystem.**

# Docker Environment

> [!NOTE]
> It is recommended to view the following ASCII image in the widescreen mode :D

```
+-------------------------------------------------------------------------------------------------------------------------+  +------------------------+
| Docker Desktop                                                                                                          |  | Registry               |
|                                                                                                                         |  | (e.g. Dockerhub)       |
| +-----------------------------------------------+  +------------------------------------------------------------------+ |  |                        |
| | Client                                        |  | Linux Virtual Machine                                            | |  | +--------------------+ |
| |                                               |  |                                                                  | |  | | My Container       | |
| | +-------------------------------------------+ |  | +--------------------------------------------------------------+ | |  | | Image 1            | |
| | | Docker CLI (docker)                   (*) |-|--|-> Docker API                                               (*) | | |  | +--------------------+ |
| | +-------------------------------------------+ |  | |--------------------------------------------------------------| | |  | +--------------------+ |
| |                                               |  | | Docker Daemon (dockerd) (manages img, cont, vol, etc.)   (*) |-|-|--| | My Container       | |
| | +-------------------------------------------+ |  | +--------------------------------------------------------------+ | |  | | Image 2            | |
| | | Graphical User Interface                  | |  |                                                                  | |  | +--------------------+ |
| | |                                           | |  | +----------------+        +---------------------+                | |  | +--------------------+ |
| | | [ GUI Screen View ]                       | |  | | Container 1a   |------->| My Container Image 1|                | |  | | nginx  [N]         | |
| | |                                           | |  | +----------------+      / +---------------------+                | |  | +--------------------+ |
| | |                                           | |  |                        /                                         | |  | +--------------------+ |
| | +-------------------------------------------+ |  | +----------------+    /   +---------------------+                | |  | | ubuntu [Logo]      | |
| |                                               |  | | Container 1b   |---'    | My Container Image 2|                | |  | +--------------------+ |
| | +-------------------------------------------+ |  | +----------------+        +---------------------+                | |  +------------------------+
| | | Docker Credential Helpers                 | |  | +--------------------------------------------------------------+ | |
| | +-------------------------------------------+ |  | | K8s Cluster (kubeadm)                                        | | |  +------------------------+
| |                                               |  | |                                                              | | |  | Part of                |
| | +-------------------------------------------+ |  | |                  kubernetes                                  | | |  | "Docker Engine"        |
| | | Extensions                                | |  | |                                                              | | |  | (Open Source)      (*) |
| | +-------------------------------------------+ |  | +--------------------------------------------------------------+ | |  +------------------------+
| +-----------------------------------------------+  +------------------------------------------------------------------+ |
+-------------------------------------------------------------------------------------------------------------------------+
```

# Docker vs Virtual Environments

Python virtual environments (`venv`, `conda`, etc.) and Docker containers both solve the core problem of isolation, but they operate at completely different levels of the stack.

## Which approach is better?

Neither is strictly "better"—they solve different scopes of isolation, and developers actually use both together.

| Feature | Python Virtual Environment | Docker Container |
| --- | --- | --- |
| **What it isolates** | Python packages and the Python interpreter. | The entire operating system user-space (OS, C-libraries, system packages, non-Python code, networks). |
| **Dependencies** | Isolates `pip install` packages (e.g., `requests`, `pandas`). | Isolates `apt/yum` dependencies, Python versions, database binaries (e.g., PostgreSQL, Redis), system libraries (like OpenCV/CUDA). |
| **Host Dependence** | Relies on your local OS. (A Linux-compiled binary won't work inside a `venv` on Windows). | Runs the exact same Linux environment regardless of whether host OS is macOS, Windows, or Linux. |
| **Performance Overhead** | Zero (just a folder with symlinks to Python). | Minimal (lightweight virtualization via container runtime). |
| **Startup Time** | Instant. | Slower. |

## When to use which?

* **Use venvs for:** Pure Python projects (scripts, basic web scripts, data analysis) where you only need to manage Python package versions locally on your machine.
* **Use Docker for:**
  * Complex applications requiring system-level dependencies (like C++ libraries, geospatial tools, ffmpeg).
  *  Multi-service setups (e.g., a Python API + a PostgreSQL database + a Redis cache running together).
  *  Deploying code to production servers.

# Practical use

> [!NOTE]
> **Docker is predominantly an infrastructure tool for developers, DevOps engineers, and cloud systems, not non-technical end users.**

## A. In Software Development (Dev Environments)

Instead of forcing a new developer to install Python 3.11, PostgreSQL 15, and Redis on their laptop, a project includes a single configuration file (`docker-compose.yml`).

* The developer runs `docker compose up`.
* In seconds, the app, database, and background workers run in pre-configured containers on their machine.

## B. CI/CD

This is where Docker shines most:

1. **Build Once:** When code is pushed to GitHub/GitLab, an automated server builds a Docker **Image** containing the application code and all its dependencies.
2. **Test:** That exact image runs tests in the cloud.
3. **Deploy:** The exact same image is pushed to production servers (AWS ECS, Kubernetes, DigitalOcean).
Because the image in production is pixel-for-pixel identical to the image tested locally, the "it works on my machine" bug disappears.

## C. What about non-technical end users?

While regular consumers won't open a terminal and run `docker run`, they still use Docker **indirectly every day**:

* **SaaS Web Apps:** Gmail, Spotify Web, Netflix, and online banking run inside containerized environments managed by Kubernetes or Docker in the cloud.
* **Self-Hosting Community:** Tech-savvy home users use Docker Desktop/Unraid/Synology to host home automation (Home Assistant), media servers (Plex), or ad-blockers (Pi-hole) with a single click.

# Databases

Databases are notoriously fickle to install and configure. The instructions are often complex and vary across different versions and operating systems. For development, where you might need to run multiple versions of a single database or create a fresh database for testing purposes running in a container can be a massive improvement.

The setup/installation is handled by the container image, and all you need to provide is some configuration values. Switching between versions of the database is as easy as specifying a different image tag (e.g. `postgres:14.6` vs `postgres:15.1`).

A few key considerations when running databases in containers:

* **Use volume(s) to persist data**: Generally databases will store its data at one or more known paths. You should identify those and mount volumes to those locations in the containers to ensure data persists beyond the container.
* **Use bind mount(s) for additional config**: Often databases use configuration files to influence runtime behavior. You can create these files on your host system, and then use a bind mount to place them in the correct location within the container to be read upon startup.
* **Set environment variables**: In addition to configuration files many databases use environment variables to influence runtime behavior (for example setting the admin password). Identify these variables and set them accordingly.

Example command to mount volumes for postgres (https://hub.docker.com/_/postgres):

```bash
docker run -d --rm \
  -v pgdata:/var/lib/postgresql/data \
  -e POSTGRES_PASSWORD=foobarbaz \
  -p 5432:5432 \
  postgres:15.1-alpine

# With custom postresql.conf file
docker run -d --rm \
  -v pgdata:/var/lib/postgresql/data \
  -v ${PWD}/postgres.conf:/etc/postgresql/postgresql.conf \
  -e POSTGRES_PASSWORD=foobarbaz \
  -p 5432:5432 \
  postgres:15.1-alpine -c 'config_file=/etc/postgresql/postgresql.conf'
```

# Secrets

## Overview

> [!IMPORTANT]
> A **secret** is any credential or sensitive value that should not end up in a Docker image, source control, logs, or a shared build cache.

Examples are:

- Postgres password
- database URL
- API tokens or JWT signing keys
- any app credentials

You can pass the database password as a plain environment variable: `-e POSTGRES_PASSWORD=foobarbaz`. That is fine for local practice, but it is not the safest pattern for real use.


> [!IMPORTANT]
> **Secret injection** means:
> - the secret is not baked into the image
> - it is supplied when the container runs
> - the container reads it from a protected source

Typical sources:

- environment variable
- mounted file
- Docker secret
- Kubernetes secret
- cloud secret manager

> [!IMPORTANT]
> **A secret should be provided at runtime, not hard-coded into your image or repo.**

## Build-time secret vs runtime secret

### 1) Build-time secret
Used while building the image.

Example:

```dockerfile
RUN --mount=type=secret,id=secret.txt,dst=/container-secret.txt \
  echo "Loaded secret during build"
```

This is useful for:
- fetching private packages
- reading credentials needed during build
- build automation

But it is not the usual place for a Postgres password.

Why?

Because the user password is needed when the database starts, not just while the image is being built.

### 2) Runtime secret
Used when the container starts.

This is what you want for Postgres.

The official Postgres image supports this pattern:

```bash
docker run \
  -e POSTGRES_PASSWORD_FILE=/run/secrets/postgres_password \
  -p 5432:5432 \
  postgres:15.1-alpine
```

This is better than hardcoding `POSTGRES_PASSWORD=...` because the password is stored in a file that is not part of the Docker image.

## Why the password matters

A database password is not “just a variable”. It is the authentication credential.

When your app connects:

```text
app -> Postgres
```

Postgres asks:
- “Who are you?”
- “Do you know the right password?”
- “Are you allowed to access this database?”

If the password is wrong, the app cannot connect.

So the password is absolutely required. It is not useless just because it is stored in an env var.

The question is: *“How do we keep password out of places where anyone can read it?”*

## Local development
Use a `.env` file or pass environment variables from the shell, but do not commit them.

Example:

```bash
POSTGRES_PASSWORD=foobarbaz
DATABASE_URL=postgres://postgres:foobarbaz@host.docker.internal:5432/postgres
```

Then in Docker:

```bash
docker run \
  --env-file .env \
  ...
```

This is common and practical.

## 1. Quick Reference: When to Use What

| Secret Method | Best Used For | Security Level | Main Drawback / Risk |
| --- | --- | --- | --- |
| **Environment Variables (`ENV`)** | **Non-sensitive configuration** (e.g., debug modes, public URLs) | 🔴 **UNSAFE FOR SECRETS** | Leaks easily via `docker inspect` and logs. |
| **Bind Mounts** | Quick local development testing | 🟡 **Medium** | Easy to leak into images if accidentally committed. |
| **`RUN --mount=type=secret`** | Passing secrets **during image build** (e.g., npm/pip tokens) | 🟢 **High** | Requires BuildKit (enabled by default now). |
| **`_FILE` Pattern** | Passing runtime secrets via files (used with compose/Swarm) | 🟢 **High** | Requires the app to support reading from file paths. |
| **Docker Compose Secrets** | **Local dev & single-host production** with `docker-compose.yml` | 🟢 **High** | Files exist as plain text on the host machine. |
| **Docker Swarm Secrets** | **Multi-host production clusters** | 🟢 **High** | Requires Docker Swarm mode enabled. |

---

## 2. Unpacking Each Concept (Why They Exist)

### The Golden Rule of Container Security

> **Secrets must NEVER be baked into the image layers.** Once a secret is inside an image layer, it stays in the image history forever—even if you delete the file in a later step.

### A. Environment Variables (`ENV` / `-e`)

* **What it is:** Passing plain text key-value pairs (e.g., `DATABASE_URL=postgres://...`).
* **Why people use it:** It's simple and supported everywhere.
* **Why it’s dangerous for secrets:** Anyone with access to the Docker engine can run `docker inspect <container-id>` or `docker exec` and view all environment variables in plain text. Process listings (`ps aux`) and crash logs can also leak them.
* **Verdict:** **Use ONLY for non-sensitive configuration parameters.**

---

### B. Bind Mounts

* **What it is:** Mounting a host directory or file into the container at runtime using `-v /host/path:/container/path`.
* **Role in secrets:** People sometimes use this to pass local credential files (e.g., `~/.aws/credentials`) into a running development container.
* **Verdict:** Fine for local developer workflows, but clunky and insecure for production workflows.

---

### C. Build-Time Secrets: `RUN --mount=type=secret`

* **What it is:** A secure way to mount a secret file *temporarily* during `docker build`.
* **Where it’s used:** Inside your `Dockerfile`.
* **Why it’s essential:** If you need a private SSH key or NPM token to pull private dependencies *while building* the image, traditional environment variables would bake that token into the final image layer. This flag mounts the file during execution and removes it completely when the step finishes.

---

### D. Runtime Secrets: The `_FILE` Pattern

* **What it is:** An industry convention (popularized by official images like Postgres, MySQL, Redis) where an application accepts an environment variable ending in `_FILE` (e.g., `POSTGRES_PASSWORD_FILE`).
* **How it works:** Instead of passing the raw secret string in the env variable, you pass the path to the secret file mounted inside the container (e.g., `/run/secrets/db_password`). The image’s startup script reads the file content into memory.

---

### E. Docker Secrets (Compose vs. Swarm)

Under the hood, Docker mounts secret files inside containers at `/run/secrets/<secret_name>`.

* **Docker Compose Secrets (Single Host / Local Dev):**
Defined in `docker-compose.yml` under the top-level `secrets:` block. It is a convenience feature - it simulates Docker Swarm Secrets locally by providing analogical interface for accessing secret files without polluting environment variables. Compose mounts host files into the container at runtime. Great for local setup without exposing secrets in environment variables. Not encrypted.
* **Docker Swarm Secrets (Production Clusters):**
Managed using `docker secret create` (pre-created in CLI). Swarm encrypts secrets in transit and at rest in the Swarm Raft log, sending them strictly to nodes running containers which need secrets. Mounted in in-memory `tmpfs` storage (never written to disk inside the container).
    * **in transit** → when the secret is being sent between machines, it is encrypted
    * **at rest** → when Docker managers store the secret, it is encrypted
    * **raw text** → when the secret is sent from the manager to the container and written into its `tmpfs` memory, it is not encrypted anymore (because the container needs to use its raw form eventually to authenticate/validate sth)
    * **tmpfs** → temporary storage (disappears when the container disappears, kind of like RAM)
    * **Raft log** → Swarm's managers keep an encrypted record of the cluster's configuration, including secrets, that record is called the Raft log
    * **Raft** → the name of an algorithm

> [!IMPORTANT]
A Docker Swarm secret is not the same thing as secrets passed as environments variables or by bind mounts. It is a separate Docker-managed object stored by the swarm, encrypted in the swarm manager, and only delivered to the containers that explicitly need it.

# Security

There are two main considerations when it comes to container security:

1. the contents of your container image,
2. the security of the execution configuration and environment.

## Image Security

> [!IMPORTANT]
> **Image security** is all about how secure is your image, i.e. what vulnerabilities exist in your image that an attacker could exploit, e.g. how big is your attack surface area.

- Keep attack surface area as small as possible:
  - Use minimal base images (multi-stage builds are a key enabler)
  - Don’t install things you don’t need (don’t install dev deps)
- Scan images using third-party tools
- Use users with minimal permissions
- Keep sensitive info out of images and inject them at runtime instead
- Sign and verify images cryptographically
- Use fixed image tags, either:
  - Pin major.minor (allows patch fixes to be integrated)
  - Pin specific image hash

## Runtime Security

> [!IMPORTANT]
> **Runtime security** is all about how secure you are if an attacker manages to compromise a container. What can they do? Are they able to enter the host or are they securely confined within the container?

### Docker daemon (dockerd)
  - Start with `--userns-remap` option to make sure container's and host's namespaces are separated

### Individual containers
- Use read only filesystem if writes are not needed
- `--cap-drop=all` to drop all capabilities, then `--cap-add` anything you need
- Limit cpu and memory, e.g. `--cpus=“0.5”` and `--memory 1024m`, to prevent Denial of Service Attacks
- Use `--security-opt` to restrict what a containerized application can do at the system level (seccomp profiles, apparmor profiles)

# Networks

**Docker networking is the virtual wiring that allows containers to talk to each other, to your main computer, or to the outside internet.**

By default, Docker keeps containers completely isolated in their own little bubbles. Networks act as controlled bridges between those bubbles.

## The 4 Common Network Types

| Network Type | Analogy | How it Works | Best Used For |
| --- | --- | --- | --- |
| **Bridge** *(Default)* | A private Wi-Fi router inside your computer | Containers join a private virtual network. They can talk to each other by name, but are hidden from the outside world unless you open (publish) a port. | Standard apps running on a single computer (e.g., web app + database). |
| **Host** | Plugging directly into the main wall jack | The container bypasses Docker's virtual network and shares your computer's exact IP address and ports directly. | High-performance apps where speed is critical and isolation isn't required. |
| **Overlay** | A VPN connecting multiple houses | Connects containers running across different physical computers or servers into a single seamless network. | Multi-server setups (Docker Swarm / Kubernetes). |
| **None** | Unplugging the ethernet cable | Complete isolation. The container has no network connection at all. | Running isolated background tasks like data processing or security tests. |

## Practical Example: A Simple Web App

Imagine you have a web server container and a database container:

1. **Without a shared network:** The web server cannot find the database.
2. **With a custom Bridge network:**
   * You create a network: `docker network create my-app-net`
   * You attach both containers to `my-app-net`.
   * Now, the web app can instantly connect to the database using its name (e.g., `http://database:5432`) without needing to know IP addresses.

# Tips on writing Dockerfiles

Dockerfile is a textfile serving as a recipe for an image.

👨‍🍳 Application Recipe:
1. Start with an Operating System
2. Install the language runtime
3. Install any application dependencies
4. Set up the execution environment
5. Run the application

> [!NOTE]
> The process of converting a Dockerfile to an image is called **building**.
> 
> **BuildKit** is a build engine that takes a configuration file (such as a Dockerfile) and converts it into a built artifact (such as a Docker image). It uses **DAG (Directed Acyclic Graph)** data structure to represent various operations, usually file operations. In such graph, **child node** may represent a single Dockerfile command which can be executed only if all **parent nodes** of this child node finish executing, where parent nodes may represent operations such as downloading files, putting them in a given directory, etc. Multiple parent node sequences leading to the same child node can be **parallelized**, thus improving efficiency.

> [!NOTE]
> Docker allows building **multi-architecture images** which make it possible to have multiple images of a single application, each suitable for a different CPU architexture (e.g. AMD vs ARM).

To build (create) an image Docker uses both a Dockerfile and a **build context**. Build context is usually the directory with your source code.

You can include a **`.dockerignore`** file inside the build context to specify which files should be ignored by Docker when an image copies source files from your local directory into a directory inside the image.

> [!TIP]
> **Use a specific version of a base image instead of the default `latest`. Additionally, try to use lighter and more secured/restricted versions to reduce disk usage, improve security and prevent unexpected changes to your new builds due to latest upstream image being constantly updated by its provider.**

> [!TIP]
> **Set the working directory inside the container according to the conventions of your language/framework.**

> [!TIP]
> **Use the trailing slash `/` whenever your target (e.g. copying target) is a directory, especially if this directory might not exist yet. Omit the trailing slash when you want to copy a single file and you want to explicitly rename it.** 

> [!TIP]
> **First copy the application dependencies and install them. Only after that copy the remaining necessary source code files. This order helps to prevent cache invalidation (cache recreation) and speeds up the build process.**

> [!TIP]
> **Set the user inside the container to be non-root as this prevents the user of the application to have too many privileges and therefore adds another layer of security to the application.**

> [!TIP]
> **Add metadata to the image, e.g. what port the image container is expected to be listened on.**

> [!TIP]
> **Use multi-stage Dockerfiles.**

# More on multi-stage Dockerfiles

In standard Docker, every tool you use to build your app (compilers, build scripts, development tools, full SDKs) stays inside the final container image forever even though you often don't need it after building the final app.

A multi-stage Dockerfile lets you split your Dockerfile into distinct "stages." The idea is that you use heavy construction tools in stage 1 to compile your app, and then copy only the finished binary or code into a fresh, lightweight stage 2 for running it. Docker then discards everything from stage 1 leaving only lightweight stage 2.

Pros:

* reduced image sizes
* better security (less packages +  less code + less ... = smaller attack surface)
* faster deployments

You can have more than 2 stages, of course. You can also define custom dependency tree between stages by creating common base stages and using them inside subsequent stages however you like. This can be used for example to create two separate (sub)images within a single Dockerfile: one application image for development/testing process and one application image for production deployment.

## Behaviour cheatsheet

### 1. Default Behavior (No `--target` specified)

* **Goal:** Docker builds the **last stage** defined at the bottom of the Dockerfile.
* **Execution:** Docker builds the last stage and any parent stages it directly depends on (via `FROM` or `COPY --from`).
* **Skipped:** Any stages that are NOT part of the direct dependency tree of that final stage are completely ignored and skipped.

---

### 2. Targeted Behavior (`--target <stage_name>`)

* **Goal:** Docker stops immediately once the requested target stage is finished.
* **Execution:** Docker builds only up to the specified stage (plus any parent stages it relies on).
* **Skipped:** Every stage defined **after** the target stage—or on parallel branches—is completely ignored.

---

### 3. Linear vs. Parallel Stage Layouts

* **Linear (Sequential):** `Stage A` $\rightarrow$ `Stage B` $\rightarrow$ `Stage C`
  * Target `Stage B`: Builds `A` and `B`. Skips `C`.
  * Target `Stage C` (or default): Builds `A`, `B`, and `C`.


* **Parallel (Branched):** `Base` $\rightarrow$ (`Dev` **OR** `Production`)
  * Target `Dev`: Builds `Base` and `Dev`. Skips `Production`.
  * Target `Production` (or default): Builds `Base` and `Production`. Skips `Dev`.

---

### Summary Table

| Build Command | Stages Processed | Stages Skipped |
| --- | --- | --- |
| `docker build .` | Bottom-most stage + its dependencies | Any unrelated intermediate/parallel stages |
| `docker build --target <stage_name> .` | `<stage_name>` stage + its dependencies | Anything after `<stage_name>` or outside its path |

# --link

The `--link` flag in Docker's `COPY` command makes your builds **faster** and **smarter with cache** by creating files in an isolated layer instead of modifying the existing filesystem.

---

* **Without `--link` (Standard COPY):** Docker takes the current base layer, unpacks the base image, merges your new files *directly into it*, and creates a new combined layer. If the base image changes (e.g., an updated OS patch), Docker's cache breaks, and it has to copy all your files over again from scratch.
* **With `--link`:** Docker creates your copied files on a completely separate, independent "sheet" without touching the layers underneath. It then links these independent layers together at the very end.

---

* **Better Cache Reuse:** If you update your base image (e.g., `FROM node:18` to `FROM node:20`), Docker can reuse the cached layer containing your copied files/dependencies. It doesn't need to perform the copy again.
* **Parallel Downloads & Builds:** Because the layer created by `COPY --link` doesn't depend on the base image existing locally first, Docker (via BuildKit) can copy your source files in parallel while it is still downloading or building the base image.

---

* **Use `--link` when:** You are copying application code, config files, or build artifacts that don't depend on files in the destination directory already existing.
* **Avoid `--link` when:** You rely on the copied files merging with or overwriting existing system files or symlinks from previous layers in a specific way.

# `ENTRYPOINT` vs `COPY`

## Overview

Think of a Docker container as an executable program with a set of default settings:

* **`ENTRYPOINT` is *what* the container runs.** It defines the main command that always executes when the container starts.
* **`CMD` is the *default argument* passed to that command.** It provides optional flags or inputs that can be easily overridden when running the container.

In other words:

* `ENTRYPOINT` says ***“this is the command I always want to run, with optional arguments”***
* `CMD` says ***“this is the default command and arguments”***

Imagine setting up a container that plays movie files using a command-line player like `vlc`:

* **`ENTRYPOINT`** set to `vlc` means this container is built strictly to run `vlc`.
* **`CMD`** set to `sample.mp4` means that if you don't specify a video, it defaults to playing `sample.mp4`.

```dockerfile
ENTRYPOINT ["vlc"]
CMD ["sample.mp4"]

```

* **Default run:** Running `docker run my-player` executes:
`vlc sample.mp4`
* **Overriding CMD:** Running `docker run my-player action.mp4` overrides `CMD` and executes:
`vlc action.mp4`

| Feature | `ENTRYPOINT` | `CMD` |
| --- | --- | --- |
| **Primary Purpose** | Defines the fixed executable command. | Defines default arguments or a fallback command. |
| **Overriding from CLI** | Hard to override (`docker run --entrypoint ...`). | Easy to override (just append arguments to `docker run`). |
| **Common Use Case** | Single-purpose containers (e.g., database, web server, CLI tool). | Flexible containers or default flags. |

## How They Combine

1. **Both used together (Recommended pattern):** `ENTRYPOINT` defines the binary, and `CMD` supplies default flags.
```dockerfile
ENTRYPOINT ["ping"]
CMD ["8.8.8.8"]
```


* `docker run my-ping` $\rightarrow$ pings `8.8.8.8`
* `docker run my-ping 1.1.1.1` $\rightarrow$ pings `1.1.1.1`


2. **Only `CMD`:** Used when you want the container to be entirely flexible (e.g., a general-purpose Linux terminal image).
```dockerfile
CMD ["bash"]
```


* `docker run my-image` $\rightarrow$ launches `bash`
* `docker run my-image python app.py` $\rightarrow$ runs `python app.py` instead.

# Composing multiple containers

If you have one container, you can use basic `docker run` command to manage its lifecycle. But if you have more than one container instead of dealing with each one of them through the individual `docker run` commands, it is recommended to use `docker-compose.yml` file which makes managing multiple containers much easier (behind the scenes it does the same thing as `docker run` commands).

To use `docker compose`, we write a yaml file that contains all of the necessary configuration options. For each `docker run` option there is a corresponding compose yaml syntax. Within the yaml file we specify which version of the `docker compose` syntax we are using, and then create a block for each service.

```yaml
version: "3.8"
services:
  service-a:
    image: foo
    # configuration options for service-a
  service-b:
    image: bar
    # configuration options for service-b
```

# Development tips

> [!TIP]
> **Use compose files and makefiles to be able to run multiple applications and perform multiple operations via single terminal commands.**

> [!TIP]
> **Use bind mounts to connect the code from the host to the container's filesystem. This allows you to see changes to your application in real-time, without having to rebuild the images every time a change to the source code is made.**

> [!TIP]
> **Use third-party utilities that enable automatic restarting (hot reloading) every time a change is made to the source code.**

> [!TIP]
> **Attach a debugger to a containerized application to be able to inspect local variables, go through the source code line by line, etc. To attach a debugger, the containerized application should publish a debugging port to which a debugger can be attached. Otherwise, it may be impossible to debug a containerized application running in isolation from the rest of the system.**

> [!TIP]
> **Configure test suites for a containerized application by overlaying an additional `docker-compose-test.yml` file over the `docker-compose-dev.yml` file to customize the commands such that they run tests.**

> [!TIP]
> **Use CI/CD tools like GitHub Actions to automate tagging, building, testing, scanning, pushing and deploying containerized applications.**

> [!TIP]
> **For each new pull request you can use a temporary (ephemeral) environment that will be active for some short amount of time and will allow you to see how your application behaves after that new pull request. Note that such temporary environments are usually provided by third-party companies and are not usually free.**

# Deployment

## Basic definitions

* **IP Address:** Every device connected to the internet gets a unique numerical address (e.g., `192.0.2.1`). Users type your domain into a browser, which then translates it into the IP address of your hosting server.
* **Domain Name:** The human-readable address of your application (e.g., `myapp.com`). You buy these from a **Domain Registrar** (like Namecheap or GoDaddy).
* **DNS (Domain Name System):** The "phonebook" of the internet. DNS servers convert human-friendly domains into machine IP addresses.
* **SSL / TLS Certificate (HTTPS):** A security protocol that encrypts data sent between the user’s browser and your hosting server. Modern browsers flag sites without an SSL certificate as "Not Secure."
* **CDN (Content Delivery Network):** A global network of distributed servers that cache static assets (images, JavaScript, CSS) close to end users to speed up loading times (e.g., Cloudflare, Fastly).
* **Frontend:** HTML, CSS, JavaScript files rendered directly in the user's browser. Frequently hosted on static hosts or CDNs (e.g., Netlify, Vercel).
* **Backend:** Server-side code (Node.js, Python, Java, Go) that executes logic, handles authentication, and interacts with databases.
* **Database Hosting:** Dedicated hosting for persistent storage (SQL/NoSQL) like PostgreSQL, MongoDB, or MySQL (e.g., Supabase, AWS RDS, MongoDB Atlas).
* **Environment Variables:** Sensitive runtime variables (API keys, database passwords) stored securely on the hosting platform rather than hardcoded into your application source code.
* **CI/CD (Continuous Integration / Continuous Deployment):** Automated pipelines (like GitHub Actions) that test and automatically deploy code changes to your live server whenever you push changes to your source control repository.
* **Reverse Proxy / Web Server:** Software (like Nginx or Apache) running on your server that routes incoming internet requests to the correct internal port where your backend application is listening.
* **Build Process:** The step that compiles, bundles, and optimizes source code into production-ready files before hosting serves them to clients.

> [!IMPORTANT]
> **Deployment:** The actual process of building, sending, and executing your application code on a target hosting environment.

> [!IMPORTANT]
> **Hosting** is the service of storing your application's files, code, databases, and media on a physical or virtual computer called a **server** that remains constantly powered on and connected to the internet. When you host an application, you rent space on these servers so that users around the world can access your site at any time.

> [!IMPORTANT]
> **Cloud** is a set of someone else's servers/machines that you rent so that you can run your web apps and showcase them on the public internet.

> [!IMPORTANT]
> **Node** is a single computer connected to the system. It can be a physical server sitting in a rack or a Virtual Machine (VM) rented in the cloud. 1 computer = 1 node.

> [!IMPORTANT]
> **Cluster** is a group of multiple nodes linked together over a local network that act like one unified system. If you wire 4 server computers together and install Swarm software on them, those 4 computers form a 4-node cluster.

> [!IMPORTANT]
> **Docker Swarm** is a tool for container orchestration (a simpler and easier tool serving similar purposes as Kubernetes) that is used to control clusters.

> [!IMPORTANT]
> **Stack** in Docker is a group of containers that logically belong together, e.g. database + backend + frontend.

> [!IMPORTANT]
> **Downtime** is any period during which a system, website, or application is offline, unresponsive, or unavailable to users. It can occur due to unplanned events, such as hardware crashes, software bugs, and network outages, or through planned maintenance like software updates and infrastructure upgrades. Minimizing downtime is a primary goal in system administration to ensure continuous service availability and prevent lost business revenue.

> [!IMPORTANT]
> **Replica** is an identical, running copy of an application container or database instance created to distribute workload and maintain availability. In container orchestrators like Docker Swarm or Kubernetes, running multiple replicas of a service allows traffic to be load-balanced across them, ensuring that if one instance fails, the remaining replicas continue serving requests without causing downtime.

> [!IMPORTANT]
> **Load balancing** is the process of distributing incoming network traffic across multiple servers to prevent any single resource from becoming overwhelmed. By evenly spreading the workload, it optimizes application performance, reduces latency, and ensures high availability if a server fails.

> [!IMPORTANT]
> **Rolling update** is a deployment strategy that incrementally replaces old instances of an application with new ones without taking the system offline. By updating nodes or containers sequentially in batches while keeping the rest active, the application remains fully available to users throughout the process with zero downtime.

> [!IMPORTANT]
> **Health check** is a configurable command defined in a container's configuration that periodically tests whether the application running inside is actually functional, rather than just checking if its process is alive. If the command fails consecutive runs, Docker marks the container status as `unhealthy`, enabling orchestrators to automatically restart or route traffic away from the failing container.

## Overview

When you run `docker run` on your laptop, Docker spins up a container using your laptop's CPU and RAM. Perfect for development, but if your laptop turns off or gets overloaded, the app crashes. Real-world applications (like Netflix or Amazon) need hundreds of servers working together so that if one physical computer crashes, the app stays online.

The Cloud simply means someone else's servers that you rent over the internet. Instead of buying physical machine racks, setting up cooling, and plugging in power cables, you rent virtual servers (called Virtual Machines or instances) from providers like AWS (Amazon), Google Cloud (GCP), or Microsoft Azure. Deploying to the Cloud means taking the Docker container that works on your laptop and sending it to run on one or more of these rented servers accessible to the public internet.

If you rent 10 servers in the cloud to run your app, manually running `docker run` on all 10 servers and managing them individually would be a nightmare. You need a tool to manage all 10 servers as if they were **one giant computer**.

This process is called **Container Orchestration**, and **Docker Swarm** is Docker’s native orchestration tool built directly into the engine.

In a Docker Swarm cluster, your machines are split into two roles:

1. **Manager Nodes:** The "brains." They listen for your commands, monitor the health of the system, and decide which machine runs which container.
2. **Worker Nodes:** The "muscles." Their only job is to execute the containers assigned to them by the Managers.

What Docker Swarm handles automatically for you:

* **Self-Healing:** If a Worker machine crashes, Swarm automatically restarts its containers on another active machine.
* **Scaling:** Want 5 copies of your web app running? You tell Swarm `replicas: 5`, and it spreads them across your nodes.
* **Load Balancing:** When traffic comes in, Swarm routes it evenly across all working containers.

> [!TIP]
> In modern development, you will also hear about **Kubernetes (K8s)**. Kubernetes serves the exact same purpose as Docker Swarm (orchestrating containers across cloud servers), but it is more powerful, complex, and widely used in large enterprises. Docker Swarm is simpler and easier to learn first.

> [!NOTE]
> **A single container cannot be split or spread across multiple computers.**
> 
> Instead, running an app across multiple machines works by **duplicating independent copies (instances) of the container** and using an entry traffic manager to split the incoming users between them.
> 
> When you build a Docker image for your application (for example, a Python web server), that image acts like a blueprint or mold.
> 
> 1. **Duplication (Replicas):** Instead of telling Docker to run $1$ container, you tell Docker Swarm: *"I want $4$ replicas of this app."*
> 2. **Distribution:** Swarm looks at your 4-node cluster and places **1 identical container copy** onto **Node 1**, **Node 2**, **Node 3**, and **Node 4**.
> 3. **Traffic Distribution (The Load Balancer):** A tool called a **Load Balancer** sits in front of your cluster. When Users #1, #2, #3, and #4 visit `yourwebsite.com`:
    * User 1's request goes to Container Copy A (on Node 1).
    * User 2's request goes to Container Copy B (on Node 2).
    * User 3's request goes to Container Copy C (on Node 3).
    * User 4's request goes to Container Copy D (on Node 4).
> 
> To the end users, they all see the exact same website. They have no idea they are talking to completely separate copies running on different physical machines.

## Real-world example

For major platforms like Netflix, deployment is a mix of two strategies:

1. **Horizontal Scaling (Duplication):** Running 50 identical copies of the video playback container across 10 machines so 50,000 people can stream simultaneously without crashing a single server.
2. **Microservices (Decomposition):** Splitting the app into smaller, independent sub-apps (services).

For example, Netflix doesn't run one giant container for everything. They break it apart:

* **Container Service A:** Handles login and passwords (2 duplicates running)
* **Container Service B:** Handles user search (5 duplicates running)
* **Container Service C:** Streams the actual video file (100 duplicates running)

All these distinct containers run side-by-side across the nodes in the cluster, communicating with each other over internal network lines.

> [!WARNING]
> You do **NOT** start one running container on Machine A and then try to copy or clone that running container over to Machine B.
> 
> Instead, **you create multiple, independent containers based on the exact same Docker Image** pulled from a registry.

> [!WARNING]
> Note that in case of complex apps with many containers and many clusters, **the access to the central database needs to be carefully handled and synchronized**.

## Docker Swarm in practice

Docker Swarm turns multiple Docker hosts (machines) into a single, virtual Docker engine called a **cluster**. **Docker Swarm can reuse your `docker-compose.yml` file to run multi-container applications across an entire cluster.**

* **Node:** An individual machine running Docker inside the cluster.
  * **Manager Node:** Receives commands, maintains cluster state, and decides where to run tasks.
  * **Worker Node:** Receives work assignments (containers) from Manager Nodes and executes them.
* **Service:** The definition of how a container should run across the cluster (e.g., "Run 3 instances of my Node.js app image from Docker Hub").
* **Task:** A single running container managed by a Service. If a container dies, Docker Swarm automatically starts a new task to replace it. This is not a standalone container - it is instantiated and managed by its template which is called Service.
* **Overlay Network:** A virtual network spanning across all nodes in the cluster so containers on different physical machines can communicate securely using container names.

> [!TIP]
> cluster = swarm

> [!TIP]
> task = an instance of a service

For local practice on a single machine:

1. Get an access to a virtual machine provided by your cloud provider.
2. Set up firewall to allow inbound traffic (data entering the network) on the necessary ports.
3. Make sure Docker Engine is installed on that machine.
4. Initialize Docker Swarm there.
5. Configure it so that zero-downtime-rolling-updates deployment strategy is enabled, periodic healthchecks are performed and secrets are natively handled.
6. Run your container as a single node swarm cluster.

Note that in reality for simple practice you can skip purchasing a virtual machine from a cloud provider and use your own device instead.

> [!TIP]
> You can "talk" to your remote machine as if it was your local device by setting `DOCKER_HOST` variable appropriately.

> [!WARNING]
> You may want to move your database to an external storage or create backups for it in case your swarm crashes.

> [!NOTE]
> For multi-node swarm clusters access to the central database from many nodes must be handled more carefully and may require more work than in the case of a single node swarm cluster.

You can complete this whole tutorial on your local machine using a single-node swarm.

### 1. Initialize the Docker Swarm

Turns your local Docker Engine into a Swarm Manager.
Run the following command in your terminal:

```bash
docker swarm init
```

Docker will output a message confirming your node is now a Swarm Manager. It will also print a `docker swarm join --token ...` command, which you would run on other machines if you wanted to join worker nodes to this manager.

By default, when you initialize a Docker Swarm on a single machine, your node automatically acts as **both** a Manager and a Worker at the same time.

In this setup:

* **As a Manager:** It handles administrative tasks, tracks cluster state, and schedules where containers should run.
* **As a Worker:** It executes the actual container tasks (replicas) side-by-side with its management duties.

While production environments usually dedicate powerful, separate machines strictly to management (disabling worker workloads on manager nodes), combining both roles on a single machine is standard and ideal for local development, testing, and learning Docker Swarm.

### 2. Prepare Your Docker Compose File for Swarm Stack

Convert `docker-compose.yml` to a Docker Stack format.

In standard Docker Compose, you build images locally.

**In Docker Swarm, services must pull pre-built images from a container registry like Docker Hub.**

Create a file named `docker-stack.yml`, for example:

```yaml
services:
  webapp-api:
    networks:
      webapp-net:
        aliases:
          - api-node
    env_file:
      - ./webapp-db/.env
    secrets:
      - external-swarm-secret
      - non-external-secret
    ports:
      - 3000:3000
    image: 'my_username/docker-playground:20260924-zccbbaa'
    deploy:
      mode: replicated
      replicas: 3
      update_config:
        order: start-first
    healthcheck:
      test: [ "CMD", "node", "/usr/src/app/healthcheck.js" ]
      interval: 30s
      timeout: 5s
      retries: 3
      start_period: 10s
networks:
  webapp-net:
    name: webapp-net
secrets:
  external-swarm-secret:
    external: true
  non-external-secret:
    file: ./webapp-db/secret.txt
```

### 3. Practice

Deploy your stack named, for example, `my-app`:

```bash
docker stack deploy -c docker-stack.yml my-app
```

View your active services and replica count:

```bash
docker stack services my-app
```

View exact container tasks running across nodes:

```bash
docker service ps my-app_webapp-api
```

Dynamically scale containers without downtime. Increase your backend service from 2 to 5 containers on the fly:

```bash
docker service scale my-app_webapp-api=5
```

Run `docker service ps my-app_webapp-api` to watch Docker Swarm instantly spin up 3 new tasks.

Watch Docker Swarm automatically recover killed containers. Find a backend container ID using `docker ps` and manually kill it with `docker container kill <ID>`. Run `docker service ps my-app_webapp-api` immediately. You will see that Docker Swarm detected the dead container and immediately launched a new replacement task to maintain your requested replica count.

### 4. Finish

Remove the stack and leave Docker Swarm mode, remove all services, tasks, and networks created by the stack:

```bash
docker stack rm my-app
```

Turn off Docker Swarm mode on your machine:

```bash
docker swarm leave --force
```

## Compose vs. Swarm Quick Reference

| Feature | `docker compose up` (Compose) | `docker stack deploy` (Swarm) |
| --- | --- | --- |
| **Target** | Single machine | Multi-node cluster |
| **Image Source** | Builds locally or pulls | Must pull from registry (Docker Hub) |
| **Scaling** | Manual container count | `deploy.replicas` declarative scaling |
| **High Availability** | No automatic recovery if host fails | Automatically re-schedules dead tasks |
| **Load Balancing** | None builtin | Builtin routing mesh balances incoming traffic |
| **Zero Downtime Support** | No | Yes |
| **Rollback mechanism** | No | Yes |
| **Native support for secrets** | No | Yes |
