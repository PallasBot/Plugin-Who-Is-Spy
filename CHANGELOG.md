# 更新日志

本文件依据 git tag 历史整理，版本号遵循[语义化版本](https://semver.org/lang/zh-CN/)。
新提交合入后请在 `## [Unreleased]` 下记录，发布时随版本 tag 归档。

## [Unreleased]

## [4.0.17] - 2026-07-26

- feat(config): WebUI 配置字段增加 ui_group 分组与 ui_order 排序


## [4.0.16] - 2026-07-25

- feat: 声明群口令 `llm_tools`，供闲聊 selective 工具调用
## [4.0.15] - 2026-07-25

- feat: PluginMetadata.extra 增加 `help_tag`（帮助图分组）

## [4.0.12] - 2026-07-13

- docs(copy): 非好友须先私聊牛牛提示去掉协议端名称，统一面向用户表述

## [4.0.11] - 2026-07-13

- docs(copy): 补充非好友须玩家先私聊牛牛一次才能收词/投票的提示（开房、加入、发词与排障文案）

## [4.0.10] - 2026-07-12
- feat(vote): 私聊投票说明附带本轮述词总结

## [4.0.9] - 2026-06-27
- docs(readme): 命令权限默认等级改用中文展示

## [4.0.8] - 2026-06-27
- docs(readme): 「怎么使用」口令统一加行内代码标记

## [4.0.7] - 2026-06-24
- feat(knowledge): 声明 knowledge_sources FAQ 供 LLM 注入

## [4.0.6] - 2026-06-19
- docs(assets): 更新头像资源并改用 PyPI 版本徽章
- chore(assets): 替换品牌头像为透明背景版本

## [4.0.5] - 2026-06-18
- docs(readme): 统一官方插件卡片模板

## [4.0.4] - 2026-06-18
- refactor(deliver): 精简投递逻辑并更新安装文档

## [4.0.3] - 2026-06-18
- migrate: src.* → pallas.api.* / pallas.product.* / pallas.core.*
- release: bump to 4.0.3 for pallas import migration

## [4.0.2] - 2026-06-18
- docs(readme): 添加 Pallas-Bot hero 图
- chore(release): 4.0.2 同步 README 进 PyPI 包

## [4.0.1] - 2026-06-17
- feat: Pallas-Bot 4.0 官方扩展首包
- fix(build): 修正 hatch wheel 的 src 包路径
- feat(release): PyPI 发版 workflow 与 4.0.1
