#!/usr/bin/bash

sudo corepack enable

sudo chown -R 1000:1000 /workspace node_modules .pnpm-store \
  && pnpm install-completion bash \
  && pnpm install