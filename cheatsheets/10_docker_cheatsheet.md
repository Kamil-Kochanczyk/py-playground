# Commands

- `docker system df` - show disk space usage
- `docker system prune` - delete unused data
- `docker run <user>/<name>:<tag>` - create and run a container from an image
- `docker run -i -t [--rm] [--name <container_name>] [-v <volume_name_or_local_path>:<where_to_mount_inside_container_filesystem] <image, e.g. ubuntu:latest>` - run a container based on an image
  - `-i` and `-t` add a pseudo, interactive terminal, this terminal has the possibility to take input (`-i`) and behaves like a real terminal (`-t`)
  - `--rm` means that the container and its anonymous volumes will be deleted after the container exits
  - `--name` specifies name of the container
  - `-v` mounts (maps) a volume or a host's filesystem path to the virtual path visible inside the container
    - for volume mounts the option with `-v` could look for example like this: `-v my-volume:/my-container-dir`
    - for bind mounts the option with `-v` could look for example like this: `-v ${PWD}/mylocaldir:/my-containerdir`, where `PWD` means "Present Working Directory"
- `docker images` - list all images
- `docker container ls -a` - list all containers
- `docker start <container_name>` - start the specified stopped container
- `docker stop <container_name>` - stop the specified running container
- `docker attach <container_name>` - attach STDIN, STDOUT and STDERR to the given container (in practice it enters the container's pseudo terminal)
- `docker build -t <image_name> <directory with Dockerfile inside>` - start the process of building (creating a container based on an image)
- `docker volume create <volume_name>` - create a new volume for storing persisting data

# 3 most important Docker ideas

> [!TIP]
> **Enveloping/Containerization**
> 
> Instead of telling someone:
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
> Programs should be lightweight and cacheable, easy to distribute and share, easy to extend or to use as building blocks inside other programs, and possible to run the same everywhere (on every machine).

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

It doesn't matter what Python you have installed on your operating system, for example, because your application isn't using the host's Python installation. It uses the Python packaged in the image and running inside the container. The host operating system still matters for providing actual physical resources, but the application environment becomes much more controlled and reproducible and more easily distribuable on across different machines.

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

The hypervisor gives each VM **virtual hardware**, it **schedules (maps) virtual hardware to physical hardware over time**.

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

> **A container packages an application together with the things the application needs from user space.**

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
> * **Dockerfile = textfile defing an image** (analogy: my_class.py)
> * **Image = blueprint** (analogy: class)
> * **Container = running instance of that image** (analogy: instance of a class)

> [!TIP]
> Other useful terms:
> 
> * **Registry (e.g., Docker Hub):** A centralized repository for storing and sharing images. You *pull* pre-built images (like Node.js, PostgreSQL, or Nginx) from a registry and *push* your custom images to it.
> * **Docker Compose:** A tool that uses a YAML configuration file (`docker-compose.yml`) to define and run multi-container applications (e.g., spinning up a web app, a Redis cache, and a Postgres database simultaneously with one command).

## Dockerfile

It is a file that defines step by step how to build (create) an image and what should happen at start when a container is created based on that image and starts running.

## Image

An image is essentially a packaged template for creating containers. It can shared so that others can download it and use it or extend it by including it in other images.

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

> [!NOTE]
> The **container runtime** is the software responsible for actually creating and running containers.

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

* namespaces
* `cgroups`
* layered filesystem

> [!TIP]
> A **partition** in Linux is a distinct section of a physical hard drive or solid-state drive that acts as an independent storage unit.

> [!TIP]
> A **network share** in Linux is a folder or directory hosted on one computer that other devices on the same network can access, read, and write to as if the files were on their own local hard drive.

> [!TIP]
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

The same idea applies to networking, where a Python program might think: *"I have my own networking interface"*, while in reality this is just a **mapping between host's `(IP_1, port_1)` and container's `(IP_1', port_1')`**.

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

## `cgroups`

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

A filesystem is basically the thing that lets an operating system organize files and directories on a disk:

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

The important thing is:

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

This answers:

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

The important thing is that this layer cannot actually modify files. So how can it be writable? The idea is that this writable layer stores the result of **temporary changes (deltas) of files** which are created when the given container is running. They are applied from bottom to top. They can also be created at runtime and then get immediately destroyed when the container stops running, thus always preserving the original state of all read-only layers.

The deltas to files are actually applied to all layers, from the most bottom layer, to the most top layer (the writable layer).

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

When the container starts, runtime presents the resulting layers, with all deltas applied, as a unified filesystem:

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
        │ Layer C (reado-only)│
        ├─────────────────────┤
        │ Layer B (reado-only)│
        ├─────────────────────┤
        │ Layer A (reado-only)│
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

as normal.

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
> **Layers can be seen also as filesystem changes/deltas.**

The fact that writable layer is temporary and just read-only layers persist when container dies means that data stored inside the container's writable layer is inherently **ephemeral**, i.e. **data saved or generated when a container is running will be deleted when the container dies**.

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

**Modifying the contents of a container at runtime is not something you would normally do.**

> [!TIP]
> For anything we need in the container at runtime we should build it into the image! The one exception to this rule is environment specific configuration (environment variables, config files, etc...) which can be provided at runtime as a part of the environment.

> [!TIP]
> Volumes and mounts allow us to specify a location where data should persist beyond the lifecycle of a single container. The data can live in a location managed by Docker (volume mount), a location in your host filesystem (bind mount), or in memory (tmpfs mount).

> [!TIP]
> This third option (tmpfs mount) does not persist the data after the container exits, and is instead used as a temporary store for data you specifically DON'T want to persist (for example credential files). It is included here for completeness but should not be used for application data you want to persist.

# Low level explanations of Docker concepts

## Dockerfile

> [!IMPORTANT]
> **A recipe for constructing this filesystem and defining how to start the resulting process**.

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

> **Put this file into the image filesystem (into the working directory).**

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

> "It basically builds a stack of filesystem changes."

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
> **Container = a process using Linux resources = isolated views of system resources + resource limits + a specially constructed filesystem based on an image = image read-only layers plus writable layer seen as one filesystem.**

# Docker Environment

> [!NOTE]
> It is recommended to view the following ASCII image in widescreen mode :D

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
| **Startup Time** | Instant. | Seconds. |

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

Instead of forcing a new developer to install Python 3.11, PostgreSQL 15, and Redis on their laptop—which takes hours and risks configuration conflicts—a project includes a single configuration file (`docker-compose.yml`).

* The developer runs **`docker compose up`**.
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
