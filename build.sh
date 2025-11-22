#!/bin/bash
# Koyeb用のビルドスクリプト

echo "Installing Node.js dependencies..."
npm install

echo "Building React app..."
npm run build

echo "Build completed!"

