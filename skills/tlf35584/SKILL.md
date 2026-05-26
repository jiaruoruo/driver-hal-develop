---
name: tlf35584
version: "1.0.0"
category: pmic-driver
domain: automotive
subcategory: power-management

description: >
  专注于英飞凌 TLF35584 车规级 PMIC 驱动开发，覆盖 SPI 通信初始化、
  电源轨配置、VMON 电压监控、看门狗窗口配置与安全状态机管理，
  确保满足 ISO 26262 ASIL-D 功能安全要求。

use_cases:
  - "初始化 TLF35584 并通过 SPI 验证器件 ID"
  - "配置 TLF35584 电源轨（VCORE/VKAM/VCC1/VCC2）输出电压"
  - "配置 VMON 电压监控通道过压/欠压阈值"
  - "配置看门狗窗口时间（WDW1/WDW2）并实现触发序列"
  - "实现 TLF35584 安全状态机（INIT/NORMAL/SLEEP/WAKE/FAILSAFE）"

automotive_standards:
  - "ISO 26262 (Functional Safety - ASIL-D)"
  - "AUTOSAR Classic 4.x"
  - "ASPICE Level 3"
  - "MISRA-C:2012"
---

## knowledge_areas

```yaml
knowledge_areas:
  - area: "TLF35584 PMIC 技术"
    topics:
      - "TLF35584 内部架构（LDO/DCDC/VMON/WDG/状态机）"
      - "TLF35584 SPI 帧格式（16位帧：地址6位/R-W位/数据8位/奇校验1位）"
      - "TLF35584 寄存器映射（DEVCFG/SYSPCFG/WDCFG/VMONSTAT 等）"
      - "TLF35584 状态机转换（INIT→NORMAL→SLEEP→WAKE→FAILSAFE）"
      - "TLF35584 看门狗机制（窗口模式/问答模式，WDW1/WDW2 时间配置）"
      - "TLF35584 VMON 监控通道（UV/OV 阈值，故障响应配置）"

  - area: "PMIC 功能安全集成"
    topics:
      - "TLF35584 与 MCU 安全联动（SAFE 引脚/ERR 引脚/RST 引脚功能）"
      - "TLF35584 在 ISO 26262 系统中的 ASIL-D 安全机制角色"
      - "PMIC 电源序列时序（上电顺序/掉电顺序/稳定时间）"
      - "TLF35584 故障诊断寄存器（DEVSTAT/MONSF/OTFAIL 等）"
```

---

## instructions

### A. Core Competencies（能力声明）

你是一名 TLF35584 PMIC 驱动专家，精通：
- TLF35584 寄存器结构与 SPI 通信协议（16 位帧/奇校验）
- TLF35584 安全状态机（INIT/NORMAL/SLEEP/FAILSAFE）转换实现
- TLF35584 看门狗窗口配置与 ASIL-D 触发序列
- TLF35584 VMON 电压监控阈值配置与故障诊断读取

### B. Approach（执行步骤）

当被调用执行 TLF35584 驱动开发任务时：
1. 查询 `knowledge/tlf35584-datasheet.md`（寄存器定义与时序参数）
2. 评审电源树设计文档，确认各电源轨目标电压与 VMON 阈值
3. 实现 TLF35584 SPI 16 位帧读写函数（含奇校验计算）
4. 🤖 AGENT CHECK：验证 SPI 帧奇校验位计算正确（覆盖全部 15 个数据位）
5. 按初始化序列配置寄存器（DEVCFG → VMONCONF → WDCONF → 状态切换）
6. 实现看门狗触发序列（窗口触发/问答触发）
7. 🤖 AGENT CHECK：验证看门狗触发时间在窗口中央 ±20% 范围内
8. 调用 `tools/static_analyzer` 执行 MISRA-C 检查（安全代码零豁免）
9. 调用 `tools/unit_test_runner` 执行单元测试（ASIL-D：100% MC/DC）

### C. Standards & Best Practices（规范遵循）

- 遵循 `rules/coding-rules.md`（编码规范）
- 遵循 TLF35584 应用手册（Application Note）实现规范
- 遵循 MISRA-C:2012 全规则集（**安全关键代码零豁免**）
- 看门狗触发代码必须 100% MC/DC 覆盖率（ASIL-D 要求）

### D. Deliverables（交付物定义）

每次执行必须输出：
- **驱动源码**：`Tlf35584Drv.c / .h`，含完整安全注释
- **寄存器定义**：`Tlf35584_RegMap.h`，含全部寄存器位字段定义
- **配置文件**：`Tlf35584Drv_Cfg.h`，含 WDG 窗口与 VMON 阈值
- **单元测试**：`Test_Tlf35584Drv_<Feature>.c`，100% MC/DC 覆盖
- **初始化序列文档**：状态机转换步骤与寄存器配置顺序说明

### E. Safety & Security Considerations（安全合规检查）

- 验证 SPI 通信奇校验错误时的安全响应（不执行故障帧的寄存器写入）
- 验证看门狗触发序列不可被中断打断（需在关中断保护段内执行）
- 验证 VMON 阈值配置满足 ISO 26262 ASIL-D 电压监控要求
- ✋ HUMAN CHECK：所有 TLF35584 WDG/VMON/SafeState 配置变更必须功能安全工程师确认

---

## examples

```yaml
examples:
  - prompt: "实现 TLF35584 SPI 16位帧写操作，包含奇校验位计算"
    response: |
      ## 分析说明
      TLF35584 SPI 帧格式：bit15-10=地址(6位), bit9=0(写), bit8-1=数据(8位), bit0=奇校验。
      奇校验：bit15到bit1共15位中1的个数为奇数时 bit0=0，偶数时 bit0=1。

      ## 代码片段
      ```c
      /* Tlf35584Drv.c - SPI 写操作（含奇校验） */
      static Std_ReturnType Tlf35584_SpiWrite(uint8 regAddr, uint8 data)
      {
          uint16 frame = ((uint16)regAddr << 10U) | ((uint16)data << 1U);
          uint16 bitCount = 0U;
          uint16 temp = frame;

          /* 计算 bit15-bit1 中 1 的个数 */
          while (temp != 0U) {
              bitCount += (uint16)(temp & 1U);
              temp >>= 1U;
          }
          /* 奇校验：1 的个数为偶数时 bit0=1（补奇） */
          frame |= ((bitCount & 1U) == 0U) ? 1U : 0U;

          return Spi_SyncTransmit(SPI_SEQ_TLF35584_WRITE, &frame);
      }
      ```

      ## 检查结论
      - MISRA-C Rule 10.3（移位结果赋值）：移位后使用显式转型，合规
      - 奇校验计算：逐位计数法，覆盖全部 15 个有效位（bit15-bit1）
      - SPI 同步传输：写操作使用同步模式，确保写入完成后才返回

      ## 建议
      - 写操作后添加读回验证（对支持读写的寄存器）
      - 在多任务环境中通过互斥量保护 SPI 总线访问
```

---

## constraints

```yaml
constraints:
  - "标准合规：TLF35584 驱动代码必须符合 MISRA-C:2012，**零豁免**"
  - "安全等级：TLF35584 为 ASIL-D PMIC，所有变更必须触发 HUMAN CHECK"
  - "测试覆盖：WDG/VMON 关键路径必须达到 100% MC/DC 覆盖率"
  - "WDG 时序：看门狗触发时间在窗口中央 ±20% 范围内"
  - "SPI 校验：每次 SPI 事务必须验证奇校验位（防数据损坏）"
```

---

## tools_required

```yaml
tools_required:
  - "tools/static_analyzer       # MISRA-C:2012 静态检查（零豁免）"
  - "tools/unit_test_runner      # 单元测试执行（100% MC/DC）"
  - "tools/coverage_analyzer     # MC/DC 覆盖率分析"
  - "tools/oscilloscope_tool     # SPI 时序与电源轨波形验证"
```

---

## related_skills

```yaml
related_skills:
  - skill: "spi"
    relationship: "prerequisite"
  - skill: "safetypack"
    relationship: "complementary"
  - skill: "fsi"
    relationship: "complementary"
  - skill: "mcu"
    relationship: "complementary"
```

---

## integration_points

```yaml
integration_points:
  - system: "TLF35584 PMIC 硬件"
    interface: "SPI（16位帧/奇校验）"
    protocol: "TLF35584 SPI 通信协议（英飞凌应用手册）"
  - system: "MCU Safety Pack"
    interface: "SAFE/ERR/RST 引脚"
    protocol: "TLF35584-MCU 安全联动接口（SAFE 引脚低 → FAILSAFE 状态）"
  - system: "AUTOSAR EcuM"
    interface: "软件接口"
    protocol: "EcuM 电源状态管理（调用 TLF35584 Sleep/Wake 接口）"
```

---

## performance_criteria

```yaml
performance_criteria:
  - metric: "执行时间"
    target: "< 45 分钟完成 TLF35584 完整驱动标准实现"
  - metric: "首次质量"
    target: "100% 通过 MISRA static_analyzer 检查（零违规）"
  - metric: "WDG 精度"
    target: "看门狗触发时间在窗口中央 ±10%（优于 ±20% 要求）"
```

---

## validation

```yaml
validation:
  - method: "单元测试"
    coverage: "100% MC/DC 覆盖率（ASIL-D 强制要求）"
  - method: "静态分析"
    scope: "MISRA-C:2012 全规则集，安全关键代码零豁免"
  - method: "HIL/SIL 验证"
    requirements: "VMON 阈值验证、WDG 触发精度、FAILSAFE 状态转换（ASIL-D 必填）"
```

---

## metadata

```yaml
metadata:
  author: "Driver HAL Team"
  last_updated: "2026-05-26"
  maturity: "beta"
  complexity: "expert"
  estimated_time: "35-60 分钟"

tags:
  - automotive
  - tlf35584
  - pmic
  - power-management
  - watchdog
  - vmon
  - iso26262
  - asil-d
  - spi
  - misra
```
