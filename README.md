# Nexa Research Agent

> **AI-Powered Research Automation Platform**  
> Generate comprehensive, well-sourced research reports on any topic using advanced LLMs and web search capabilities.

[![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-green.svg)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org)
[![Redis](https://img.shields.io/badge/Redis-7.0-red.svg)](https://redis.io)
[![Stripe](https://img.shields.io/badge/Stripe-Integrated-purple.svg)](https://stripe.com)

---

## **Overview**

Nexa Research Agent is an intelligent platform that transforms your topic queries into comprehensive, well-structured research reports. It acts as a sophisticated orchestration layer, leveraging a powerful pipeline of LLM reasoning, advanced web search, and content synthesis to deliver publication-quality research in minutes.

Our service operates on a **Bring Your Own Key (BYOK)** model.
You subscribe to the Nexa platform for its speed, convenience, and structured output, while using your own API keys
(e.g., for OpenRouter, Exa.ai).
This gives you full control over your costs and model usage.

### **Key Features**

- **Intelligent Orchestration**: Sophisticated pipeline for planning, searching, and synthesizing research
- **Advanced Search**: Exa.ai integration for high-quality web search and content discovery.
- **Bring Your Own Key (BYOK)**: Use your own API keys for full cost control.
- **Iterative Research**: Multi-iteration search loops with reflection and refinement.
- **Professional Synthesis**: AI-powered report compilation with proper citations
- **Flexible Pricing**: Stripe-integrated subscription for access to the Nexa platform.

---

## **Technology Stack**

| **Component**     | **Technology** | **Purpose**                                       |
|-------------------|----------------|---------------------------------------------------|
| **Web Interface** | HTML/JS/CSS    | Client-side application                           |
| **API Framework** | FastAPI        | High-performance async API (for server deployment)|
| **LLM Provider**  | OpenRouter     | Multi-model routing (DeepSeek-R1, Claude-3, Qwen) |
| **Search Engine** | Exa.ai         | Neural web search with content extraction         |
| **Payments**      | Stripe         | Subscription management and billing               |
| **Validation**    | Pydantic v2    | Runtime type checking and data validation         |
| **Deployment**    | Docker/GitHub Pages | Containerized or Static Site Deployment      |

---

## **Getting Started**

This project can be run as a static web page directly from the `index.html` file, which is ideal for demos and GitHub Pages.

1.  **Subscribe**: Use the Stripe link on the page to subscribe.
2.  **Get Keys**: After subscribing, you will be redirected and given a Nexa Access Key. You will also need your own API keys from [OpenRouter](https://openrouter.ai/) and [Exa.ai](https://exa.ai/).
3.  **Run Queries**: Enter your keys into the application interface to begin running research queries.

---

## **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## **Support**

- **Issues**: [GitHub Issues](https://github.com/your-org/nexa-research-agent/issues)
- **Discussions**: [GitHub Discussions](https://github.com/your-org/nexa-research-agent/discussions)
- **Email**: support@nexa-research.com

---

## **Acknowledgments**

- **OpenRouter** for multi-model LLM access
- **Exa.ai** for neural search capabilities
- **Stripe** for seamless payment processing
- **FastAPI** for the excellent async framework
- **The AI Research Community** for inspiration and collaboration

---

<div align="center">

**Built by the Nexa Research Team**

[Website](https://nexa-research.com) • [Documentation](https://docs.nexa-research.com) • [Blog](https://blog.nexa-research.com)

</div>
