# 📦 Proposal and Comparative Study of Wearable Devices Applied in Warehouse Management

This project aims to propose and conduct a comparative study between different **wearable devices** to support and optimize warehouse management.

---

## ✏️ **Overview**

The project explores two innovative solutions to simplify inventory and item handling operations in warehouse environments. Each proposal focuses on a different device, highlighting its advantages and limitations.

---

## 🚀 **System Proposals**

### 📱 **Proposal 1: Smartphone Application**

A **smartphone app** was developed to use **NFC tags** for item identification in the warehouse. After scanning the tag, the operator can:

- ✅ **Remove from stock:** updates status and location of the item.
- ✅ **Store:** inserts the item into the database.
- ✅ **Detail:** displays detailed information about the item.
- ✅ **Search:** shows the path and directions from the operator’s current position to the item’s location.

---

### ⌚ **Proposal 2: Smartwatch Application**

The second proposal involves a **smartwatch app** that performs the same warehouse management functions as the smartphone app. However, instead of NFC, it uses **QR codes** to identify items, leveraging a **camera connected to a Raspberry Pi Zero 2W**.

---

## ⚙️ **Common Features**

✔️ Item identification  
✔️ Stock status updates  
✔️ Pathfinding and routing in the warehouse  
✔️ Full item details display  

---

## 💻 **Technologies Used**

- **Android**: Smartphone app development  
- **Wear OS**: Smartwatch app development  
- **Raspberry Pi Zero 2W**: QR code scanning  
- **NFC**: Quick item identification with smartphones  
- **QR Codes**: Camera-based item identification for smartwatches
- **MQTT Broker**: Mosquitto Broker for MQTT communication between the devices and the server
- **Docker**: Conteinerised application on the server
- **Node-Red**: Automation flow to manage the MQTT Broker and API requests  

---

## 🎯 **Project Goals**

The main objectives of this project are to:

✨ Evaluate the efficiency and usability of each device  
✨ Determine the best wearable device for specific scenarios  
✨ Contribute to the modernization and optimization of logistics and inventory processes  

---

## 👨‍💻 **Author**

**Lucas Samaniego Vicente - UFOP/ITV**

---
