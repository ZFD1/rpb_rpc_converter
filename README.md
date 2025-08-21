# RPB/RPC 文件格式转换工具

这是一个用于实现 RPB 和 RPC 文件格式相互转换的 Python 工具。该工具能够根据输入文件的扩展名自动执行反向转换（rpb→rpc 或 rpc→rpb）。

## 功能特点

- 自动检测输入文件类型（.rpb 或 .rpc）并执行相应的转换
- 在指定输出目录生成转换后的文件
- 保持原始文件名，仅修改扩展名
- 包含完整的错误处理和日志记录功能

## 使用方法

```bash
python rpb_rpc_converter.py <输入文件路径> <输出目录路径> [-v]
```

### 参数说明

- `<输入文件路径>`: 要转换的文件路径（.rpb 或 .rpc 格式）
- `<输出目录路径>`: 转换后文件的保存目录
- `-v, --verbose`: 可选参数，显示详细日志信息

### 使用示例

```bash
# 将 RPB 文件转换为 RPC 文件
python rpb_rpc_converter.py data/sample.rpb output/

# 将 RPC 文件转换为 RPB 文件
python rpb_rpc_converter.py data/sample.rpc output/

# 显示详细日志信息
python rpb_rpc_converter.py data/sample.rpb output/ -v
```

### 示例文件

在 `examples` 目录中提供了示例文件，可用于测试转换功能：

- `example.rpb`: RPB 格式示例文件
- `example.rpc`: RPC 格式示例文件

可以使用以下命令测试转换功能：

```bash
# 将示例 RPB 文件转换为 RPC 文件
python rpb_rpc_converter.py examples/example.rpb output/

# 将示例 RPC 文件转换为 RPB 文件
python rpb_rpc_converter.py examples/example.rpc output/
```

## 注意事项

- 输入文件必须存在且为 .rpb 或 .rpc 格式
- 如果输出目录不存在，程序会尝试创建
- 输出目录必须具有写入权限

## 转换逻辑

本工具实现了 RPB 和 RPC 文件格式之间的相互转换。这两种文件格式都用于存储遥感数据几何校正的 RPC（Rational Polynomial Coefficients）模型参数，只是格式不同，但包含的信息一致。

### RPB 文件格式

RPB 文件通常采用以下格式：

```
satId = "XXX";
bandId = "XXX";
SpecId = "XXX";
BEGIN_GROUP = IMAGE
	errBias =   1.0;
	errRand =    0.0;
	lineOffset = 	+8.787000000000000e+03
	sampOffset = 	+8.787000000000000e+03
	latOffset = 	+5.197788782488139e+01
	longOffset = 	+1.267276217581132e+02
	heightOffset = 	-3.665824527965528e+01
	lineScale = 	+8.787500000000000e+03
	sampScale = 	+8.787500000000000e+03
	latScale = 	+1.000000000000000e+01
	longScale = 	+1.000000000000000e+01
	heightScale = 	+5.036755360952578e+03
	lineNumCoef = (
		-2.489085287819830e-04,
		-1.114244712474867e+01,
		...
	);
	lineDenCoef = (
		+1.000000000000000e+00,
		...
	);
	sampNumCoef = (
		...
	);
	sampDenCoef = (
		...
	);
END_GROUP = IMAGE
END;
```

### RPC 文件格式

RPC 文件通常采用以下格式：

```
LINE_OFF :+8.787000000000000e+03  pixels
SAMP_OFF : +8.787000000000000e+03  pixels
LAT_OFF : +5.197788782488139e+01   degrees
LONG_OFF:  +1.267276217581132e+02   degrees
HEIGHT_OFF: -3.665824527965528e+01   meters
LINE_SCALE: +8.787500000000000e+03  pixels
SAMP_SCALE:  +8.787500000000000e+03  pixels
LAT_SCALE: +1.000000000000000e+01   degrees
LONG_SCALE: +1.000000000000000e+01   degrees
HEIGHT_SCALE :+5.036755360952578e+03   meters
LINE_NUM_COEFF_1:-2.489085287819830e-04
LINE_NUM_COEFF_2:-1.114244712474867e+01
...
LINE_DEN_COEFF_1:+1.000000000000000e+00
...
SAMP_NUM_COEFF_1:...
...
SAMP_DEN_COEFF_1:...
...
```

### 转换过程

1. **RPB 到 RPC 转换**：
   - 解析 RPB 文件中的参数（偏移量、比例和系数）
   - 将参数按照 RPC 文件格式重新组织
   - 生成 RPC 文件

2. **RPC 到 RPB 转换**：
   - 解析 RPC 文件中的参数
   - 将参数按照 RPB 文件格式重新组织
   - 生成 RPB 文件