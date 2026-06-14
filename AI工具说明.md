# 给大模型看的工具说明

这个文件用于告诉另一个项目里的大模型：本文件夹是一个可调用的电池数据处理工具包。

## 工具包位置

如果本文件夹已经被复制到当前项目中，工具包根目录就是：

```text
电池数据工具包
```

大模型应该在这个目录下运行命令。

## 当前可用功能

### 1. 绘制电压随时间变化曲线

用途：

```text
读取 .cex / .nda / .ndax 原始电池数据，输出电压-时间曲线。
```

输入：

```text
.cex
.nda
.ndax
```

输出：

```text
plot.svg
原文件名_voltage_time_data.xlsx
```

默认时间单位：

```text
h
```

## 推荐调用方式

在 `电池数据工具包` 目录下运行：

```bat
python -m battery_data_tool voltage-time --input "原始数据文件路径" --output-dir "输出文件夹路径" --time-unit h
```

示例：

```bat
python -m battery_data_tool voltage-time --input "D:\project\data.ndax" --output-dir "D:\project\voltage_time_result" --time-unit h
```

如果工具包目录里已经安装了 `.venv`，优先使用：

```bat
".venv\Scripts\python.exe" -m battery_data_tool voltage-time --input "D:\project\data.ndax" --output-dir "D:\project\voltage_time_result" --time-unit h
```

## 第一次使用前

如果运行时报缺少依赖，先在工具包目录下运行：

```bat
安装依赖.bat
```

或执行：

```bat
python -m pip install -r requirements.txt
```

## 大模型调用规则

1. 不要修改原始数据文件。
2. 不要把输出结果写进工具包代码目录，应该写到当前项目的数据结果目录。
3. 输出结果只需要检查 `plot.svg` 和 `*_voltage_time_data.xlsx` 是否生成。
4. 如果用户没有指定输出目录，在原始数据旁边创建一个清晰的结果目录，例如：

```text
原文件名_voltage_time_output
```

5. 如果报错提示缺少 `NewareNDA`、`matplotlib`、`pandas` 等依赖，先运行 `安装依赖.bat`。

## 判断任务是否适合调用本工具包

当用户提出以下需求时，应该调用本工具包：

```text
绘制电压随时间变化曲线
电压-时间曲线
voltage-time curve
处理 .ndax/.nda/.cex 数据
从电池原始数据导出电压时间表
```

当用户需要以下功能时，当前工具包第一版还不支持，需要说明暂未集成：

```text
充放电容量-电压曲线
Aurbach 库伦效率
CV/LSV/EIS/XRD 图
批量复杂图形排版
```

