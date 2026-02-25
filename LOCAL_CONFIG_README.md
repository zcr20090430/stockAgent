# 本地配置文件

本文件用于配置默认的 OpenAI API 参数，不会被提交到 Git 仓库。

## 使用方法

1. 复制 `local_config.json.example` 为 `local_config.json`：
   ```bash
   cp local_config.json.example local_config.json
   ```

2. 编辑 `local_config.json`，填入你的默认配置：
   ```json
   {
     "default_openai_key": "your-api-key-here",
     "default_openai_base": "https://your-api-endpoint.com/v1",
     "default_openai_model": "your-model-name"
   }
   ```

3. 运行程序时，如果选择了需要这些参数的 LLM 提供商，将自动使用这些默认值

## 配置项说明

- `default_openai_key`: OpenAI API Key 或兼容接口的 API Key
- `default_openai_base`: API Base URL（如 Moonshot、Kimi 等）
- `default_openai_model`: 模型名称

## 安全提示

⚠️ **重要**: 
- `local_config.json` 已被添加到 `.gitignore`，不会被提交
- 请勿将包含敏感信息的 `local_config.json` 分享给他人
- 建议定期更换 API Key
