# Docker Services For Super AI workshop

## Requirement for Develope

* Docker
* VSCode
* VSCode Dev Container Extension

## Clone

### For Windows without WSL
```
 git clone https://github.com/mrchoke/super-ai-services-workshop2024.git --config core.autocrlf=input
```

### For Windows in WSL, Linux and macOS

```
 git clone https://github.com/mrchoke/super-ai-services-workshop2024.git
```


## Config 
ให้ copy env-example ใน api และ ui เป็น .env แล้วปรับค่าตามต้องการได้

```
cd  super-ai-services-workshop2024
```

### For Windows without WSL
```
cp env-example .env
cp ui\env-example ui\.env
cp api\env-example api\.env

```

### For Windows in WSL, Linux and macOS
```
cp env-example .env
cp ui/env-example ui/.env
cp api/env-example api/.env
```

## Dev ด้วย VSCode Dev Container

### API

```
code api
```

### UI

```
code ui
```

** ให้กดปุ่ม Open in container


## Dev

รอจน buid เสร็จ ให้ปิด terminal เดิมแล้วเปิด terminal ใหม่ ทั้ง UI และ API


### API

```
python main.py
```

เปิดเว็บที่ http://localhost:8000 ถ้าไม่เปลี่ยน port

### UI

```
pnpm dev
```
เปิดเว็บที่ http://localhost:4173 ถ้าไม่เปลี่ยน port




## Run จำลอง Production

```
docker-compose up -d
```
