# DELL U4323QE PBP DDC

Goal: be able to set PBP mode and windows using [ddcutil](https://www.ddcutil.com/) or [BetterDisplay](https://github.com/waydabber/BetterDisplay) (or other DDC related utils).

Problem: Dell doesn't provide any documentation for this interface. One must either use the physical control on the monitor or their proprietary helper [DDPM](https://www.dell.com/support/home/en-us/product-support/product/dell-display-peripheral-manager/drivers). Neither is appropriate for automation.

# Results

## Examples with m1ddc

[m1ddc](https://github.com/waydabber/m1ddc) is a simple command-line utility to interact with DDC settings on M-series Macbooks. I'm testing on Air with an M2.

```shell
# Set primary input to USBC
./m1ddc set input 27

# Set order for PBP: USBC HDMI2 HDMI1 DP1
# top left, top right, bottom right, bottom left
./m1ddc set pbp-input 15922

# Set kvm input to the order congruent with windows
# USB3 USB1 USB2 USB4
./m1ddc set kvm 10944

# Enable PBP mode 2 by 2
./m1ddc set pbp 65

```

## Examples with ddcutil

See [docs for ddcutil](https://www.ddcutil.com/).

### PBP

```shell
# USBC, HDMI1, DP1, DP2 in a 2x2 grid
ddcutil setvcp E9 0x41 60 0x1B E8 0x4df2
```

### KVM

KVM assigns USB output port to an input (HDMI, DP, ...), one USB can be assigned to multiple inputs. Not sure how it works then.

```shell
# assign USB3 to DP1, USB4 to DP2, USB1 to HDMI2, USB2 to HDMI2
ddcutil setvcp E7 0x2c40
```

```shell
# switch to the next input
ddcutil setvcp E7 0xff00
```

## E8 (PBP order)

To generate E8 use:

```python
from enum import IntEnum

class Input(IntEnum):
    HDMI1 = 0x11  # 17
    HDMI2 = 0x12  # 18
    DP1 = 0x0F  # 15
    DP2 = 0x13  # 19
    USBC = 0x1B  # 27

def model_pbp_order(S2: Input, S3: Input, S4: Input) -> int:
    return (S2 << 0) ^ (S3 << 5) ^ (S4 << 10)

```

S2, S3, S4 - are window numbers as reported by the monitor's OSD, for example with 2x2 it's: ◰ ◳ ◲ ◱.

## E7 (KVM and KVM order)

```python
from enum import IntEnum

KVM_NEXT_INPUT = 0xFF00

class KvmUSBIdx(IntEnum):
    USB1 = 1
    USB2 = 2
    USB3 = 3
    USB4 = 4

def model_kvm_inputs_by_names(
    DP1: str,
    DP2: str,
    HDMI1: str,
    HDMI2: str,
) -> int:
    return model_kvm_inputs(
        DP1=KvmUSBIdx[DP1],
        DP2=KvmUSBIdx[DP2],
        HDMI1=KvmUSBIdx[HDMI1],
        HDMI2=KvmUSBIdx[HDMI2],
    )
```

`KVM_NEXT_INPUT` special value moves KVM to the next input, afaik there's no way to move to a selected input.

# Details

See [analyse_inputs.ipynb](analyse_inputs.ipynb).

All the values are from an Arch Linux machine, connected with the "official" Display Port cable with command

```shell
$ sudo ddcutil getvcp e8 e9 60
```

# Issues

Some E8 values just don't work.

```shell
$ sudo ddcutil setvcp E8 0x45f3
Verification failed for feature e8
```

# Credits/acknowledgments

Most of the Notebook code is by ChatGPT (gpt-4o).

[ddcutil](https://www.ddcutil.com/) - without this tool, it'd be impossible to get the values to analyze.

[BetterDisplay](https://github.com/waydabber/BetterDisplay) - I learnt about DDC existing thanks to BetterDisplay's community.

[m1ddc](https://github.com/waydabber/m1ddc) - commandline tool for Macs from the author of BetterDisplay
