# Self-Managed Kubernetes Deployment of a Python REST API on AWS

🚀 **From Zero to Production-Ready Kubernetes** – A hands-on DevOps project showcasing end-to-end container orchestration, infrastructure setup, and cloud-native deployment.

### Project Overview

I built this project from scratch to demonstrate deep understanding of modern DevOps practices. It features a **Python REST API** (FastAPI/Flask with CRUD operations) fully containerized with Docker and deployed on a **self-managed Kubernetes cluster** running on AWS EC2 instances.

This is not a simple "hello-world" deployment — I manually provisioned the infrastructure, bootstrapped the control plane with kubeadm, configured networking with Calico CNI, set up NGINX Ingress, and handled all the real-world challenges of a self-managed cluster.

### Key Highlights

- **Built a multi-node Kubernetes cluster from scratch** on AWS EC2 (Master + Worker nodes) using kubeadm and containerd.
- **Containerized a Python REST API** with multi-stage Docker builds and pushed images to Amazon ECR.
- **Deployed using Kubernetes manifests**: Deployments, Services, ConfigMaps, Secrets, and NGINX Ingress Controller for external access.
- **Achieved production-like features**: Pod scaling, service discovery, health checks, and secure networking via custom Security Groups.
- **Explored 3-tier architecture** concepts (API + potential DB layer with StatefulSet/PVC or external RDS).

### Architecture

- **Infrastructure**: AWS VPC, public subnets, EC2 t3.medium instances, custom Security Groups (opened K8s ports: 6443, 10250, etc.).
- **Container Runtime**: containerd
- **Networking**: Calico CNI
- **Ingress**: NGINX Ingress Controller
- **Application**: Python REST API (CRUD endpoints)

### What I Learned & Overcame

- Bootstrap challenges: Control plane initialization, node joining, pod sandbox errors, and networking issues.
- AWS-specific hurdles: Security group rules, image pulling from ECR, LoadBalancer vs Ingress.
- Real Kubernetes internals: kubelet, etcd, CNI plugins, and declarative deployments.

This project significantly strengthened my skills in Docker, Kubernetes, AWS, and troubleshooting complex distributed systems.

### Tech Stack

- **Languages**: Python (FastAPI/Flask)
- **Containerization**: Docker
- **Orchestration**: Kubernetes (self-managed with kubeadm)
- **Cloud**: AWS (EC2, VPC, ECR, Security Groups)
- **Networking**: Calico, NGINX Ingress
- **Tools**: Git, kubectl, kubeadm, containerd

### How to Run Locally

### Screenshots / Demo

(i will Add links to screenshots of `kubectl get all`, cluster nodes, app in browser, or a short Loom video)

⭐ **Star this repo if you found it helpful!**  
Open to feedback and collaborations.

Built with passion for learning cloud-native technologies.
