# AI 驱动的 arXiv 每日论文摘要

> 一个每日自动抓取 arXiv 论文，并利用大模型生成增强摘要的项目。

本项目基于 [dw-dengwei/daily-arXiv-ai-enhanced](https://github.com/dw-dengwei/daily-arXiv-ai-enhanced) 进行了二次开发，旨在提供一个更符合个人使用习惯的自动化流程。

---

## 每日报告索引

- [2025-10-14](data/2025-10-14.html)

---

## ✨ 项目特色

相比原项目，本项目主要有以下几点改进：

- **关键词筛选**：可以只处理包含特定关键词（如 `diffusion`, `LLM`）的论文，聚焦个人研究兴趣。
- **Prompt 和模板优化**：重新设计了 AI 提示词和 Markdown 输出模板，使摘要更具可读性。
- **流程简化**：移除了原项目中部署为 HTML 页面的相关代码，专注于生成和归档 Markdown 日报。

**最终产出**：

1. 每日抓取的原始论文数据：`data/YYYY-MM-DD.jsonl`
2. 经 AI 增强和排版的 Markdown 日报：`data/YYYY-MM-DD.md`

---

## 🚀 快速开始

只需简单几步，即可部署你自己的每日 arXiv 助手。

#### 1. 准备 API Key

本项目需要调用大模型 API 来生成摘要。推荐使用 [DeepSeek API](https://platform.deepseek.com/)，性价比较高（每日开销通常低于 0.2 元）。

1. 访问 [platform.deepseek.com/api_keys](https://platform.deepseek.com/api_keys) 创建一个新的 API key。
2. 为账户充值以确保 API 能够正常调用。
3. 记下你的 **API Key** (`sk-xxxxxxxx`) 和 **Base URL** (`https://api.deepseek.com`)。

#### 2. Fork 本仓库

点击仓库右上角的 **Fork** 按钮，将此项目复制到你自己的 GitHub 账户下。

#### 3. 配置仓库 Secrets 和 Variables

##### A. 添加Secrets

进入你 Fork 后的仓库（注意是仓库的**Settings**，而不是账户的**Settings**），依次点击 **Settings → Secrets and variables → Actions**。在 **Secrets** 选项卡下，点击 **New repository secret**，添加以下 Secrets：

```
OPENAI_API_KEY=sk-xxxxxxxx # 步骤 1 中获取的 DeepSeek API Key
OPENAI_BASE_URL=https://api.deepseek.com
```

> **重要提示**:
>
> - `OPENAI_API_KEY` 是敏感信息，必须存储在 **Secrets** 中。
> - 其他非敏感配置信息存储在 **Variables** 中。

**填写示例：**
![Secrets](https://raw.githubusercontent.com/ValoraY/blog-imgs/main/img/202510111508218.png)

##### B. 添加 Variables

在仓库的 **Settings → Secrets and variables → Actions** ，在 **Variables** 选项卡下，点击 **New repository variable**，添加以下 Variables：

| 变量名       | 示例值                      | **说明**                                                     |
| ------------ | --------------------------- | ------------------------------------------------------------ |
| `CATEGORIES` | `cs.AI,cs.CL,cs.CV`         | **必需**。你关注的 arXiv 领域，用逗号分隔。分类代码可参考[此列表](https://blog.csdn.net/weixin_42906066/article/details/83863271)。 |
| `LANGUAGE`   | `Chinese`                   | **必需**。AI 生成摘要的目标语言。                            |
| `MODEL_NAME` | `deepseek-chat`             | **必需**。调用的模型名称，请确保与你的 API 平台兼容。        |
| `EMAIL`      | `user@example.com`          | **必需**。你的 GitHub 关联邮箱，用于 Git 提交。              |
| `NAME`       | `YourGitHubUsername`        | **必需**。你的 GitHub 用户名，用于 Git 提交。                |
| `KEYWORDS`   | `diffusion,transformer,LLM` | **可选**。你感兴趣的关键词，用英文逗号分隔。如果设置，将只处理标题或摘要中包含这些词的论文。 |

**填写示例：**
![Variables](https://raw.githubusercontent.com/ValoraY/blog-imgs/main/img/202510111508175.png)

#### 4. 手动运行与测试

在你完成上述所有配置后，可以手动触发一次工作流来验证设置是否正确。

1.  进入你 Fork 后的仓库页面，点击上方的 **Actions** 选项卡。
2.  在左侧的工作流列表中，点击 **arXiv-daily-ai-enhanced**。
3.  在右侧，你会看到一个 **Run workflow** 的按钮，点击它即可手动启动任务。

请注意，工作流完整运行一次可能需要较长时间，请耐心等待其完成。默认情况下，此工作流会每日自动运行，你可以在 `.github/workflows/run.yml` 文件中修改定时设置。

**运行示例：**
![workflow](https://raw.githubusercontent.com/ValoraY/blog-imgs/main/img/202510111525358.png)

#### 5. 启用 GitHub Pages

1. 进入仓库 **Settings → Pages** 页面。
2. 在 **Build and deployment** 下，将 Source 设置为 **Deploy from a branch**。
3. 将 Branch 设置为 `main` 分支和 `/(root)` 目录，然后点击 **Save**。
4. 等待片刻，你的日报索引页即可通过 `https://<你的用户名>.github.io/<仓库名>` 访问，比如我的访问链接为：https://hppeace.github.io/arXiv-daily/ (注意大小写要和仓库一致)

配置完成后，GitHub Actions 会根据预设时间自动运行，生成每日报告。

---

## ⚙️ 工作流程

项目通过 GitHub Actions 自动化执行，完整流程如下：

1. **数据抓取 (Fetch)**
   - **触发时间**: 每日 UTC 01:30 (北京时间 09:30) 自动运行。 *(注：由于Github Actions存在排队延迟，一般在北京时间 10:30 左右完成。（为什么不设置更早？因为考虑到 arXiv 发布时间，太早的话 arXiv 当天最新论文还没有发布完整）)*
   - **执行脚本**: `fetch/fetch.py`
   - **任务**: 抓取 `CATEGORIES` 中指定领域的最新论文，并保存为 `data/YYYY-MM-DD.jsonl`。
2. **AI 摘要增强 (Enhance)**
   - **执行脚本**: `ai/enhance.py`
   - **任务**: 读取原始数据，调用大模型 API 对论文进行总结和润色。如果设置了 `KEYWORDS`，则会先进行筛选。
   - **定制**: 可通过修改 `ai/system.txt` (系统提示) 和 `ai/template.txt` (单篇论文处理模板) 来调整 AI 的输出风格。
3. **生成 Markdown 报告 (Convert)**
   - **执行脚本**: `to_md/convert.py`
   - **任务**: 将 AI 生成的增强内容转换为格式化的 Markdown 文件 `data/YYYY-MM-DD.md`，并更新 `index.md` 索引页。
   - **定制**: 可通过修改 `to_md/paper_template.md` 来调整单篇论文在报告中的展示样式。

---

## 🔧 深入定制

- **更改运行时间**: 编辑 `.github/workflows/run.yml` 文件中的 `cron`表达式。
- **修改 AI 提示词**: 编辑 `ai/system.txt` 和 `ai/template.txt`。
- **调整报告模板**: 编辑 `to_md/paper_template.md`。

---

## 💻 本地运行与调试

如果你希望在本地环境中运行或调试代码，请遵循以下步骤：

1. **创建虚拟环境并安装依赖**

   ```
   curl -LsSf https://astral.sh/uv/install.sh | sh
   uv sync # 创建虚拟环境 .venv，安装 pyproject.toml 中的所有依赖
   source /var/xxx/xxx/arXiv-daily/.venv/bin/activate # 激活虚拟环境
   ```
   
2. 设置环境变量

   在终端中执行以下命令，设置必要的环境变量。

   ```
   export OPENAI_API_KEY="sk-xxxxxxxx" # 替换为你的真实 API Key
   export OPENAI_BASE_URL="https://api.deepseek.com"
   export LANGUAGE="Chinese"
   export CATEGORIES="cs.AI,cs.CL,cs.CV"
   export MODEL_NAME="deepseek-chat"
   export KEYWORDS="diffusion,transformer,LLM"
   export EMAIL="your_email@example.com" # 替换为你的 GitHub 邮箱
   export NAME="YourGitHubUsername" # 替换为你的 GitHub 用户名
   ```
   
3. 运行主脚本

   执行 run.sh 脚本来启动完整的任务流程。

   ```
   bash run.sh
   ```

---

## 📚 相关工具

- [ICML, ICLR, NeurIPS 等会议论文列表](https://dw-dengwei.github.io/OpenReview-paper-list/index.html)

---

## 🤝 致谢

- 感谢 [dw-dengwei/daily-arXiv-ai-enhanced](https://github.com/dw-dengwei/daily-arXiv-ai-enhanced) 提供了优秀的基础项目。
