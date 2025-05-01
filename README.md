# Azure Voice Bot – User Registration Assistant

This project is part of the "Advanced Topics in Cloud Computing" course (Summer Semester 2025) by Prof. Dr.-Ing. Florian Marquardt.

## Project Objective

Develop a voice bot using Microsoft Azure services that guides users through a natural language conversation to register a new account by collecting:

- Personal details (first name, last name, date of birth)
- Contact information (email, phone)
- Address (street, zip code, city, country)

Collected data will be validated and securely stored in an Azure SQL database.

---

## Technologies and Services Used

- **Azure Bot Service**
- **Azure Speech Services**
- **Azure Language Understanding (LUIS)**
- **Azure SQL Database**
- **Azure App Service**
- **Azure Key Vault** (for secret management)
- **Bot Framework SDK** (Python)

Project architecture is illustrated in the `/diagrams/architecture/` folder with draw.io, PNG and PDF formats.

---

## Repository Structure

```
azure-voice-bot/
│
├── README.md
├── docs/
│   └── dialog_flow.drawio
├── diagrams/
│   ├── dialog_flow.png
│   └── architecture/
│       ├── azure_architecture.drawio
│       ├── azure_architecture.png
│       └── azure_architecture.pdf
├── src/
│   └── (bot source code to be added here)
```

---

## Milestones

| Milestone     | Due Date | Description                                 |
|---------------|----------|---------------------------------------------|
| Milestone 1   | 06.05.25 | Concept paper, dialog flow, Azure setup     |
| Milestone 2   | 27.05.25 | Working prototype + basic database          |
| Final Version | 01.07.25 | Full bot implementation + presentation/demo |

---

## ✍️ Author

Abderrahman Moustafa  
M.Sc. Student – Software Architecture  
Brandenburg, Germany
