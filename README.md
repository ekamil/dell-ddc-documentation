# DELL U4323QE PBP DDC

Goal: be able to set PBP mode and windows using [ddcutil](https://www.ddcutil.com/) or [BetterDisplay](https://github.com/waydabber/BetterDisplay) (or other DDC related utils).

Problem: Dell doesn't provide any documentation for this interface. One must either use the physical control on the monitor or their proprietary helper [DDPM](https://www.dell.com/support/home/en-us/product-support/product/dell-display-peripheral-manager/drivers). Neither is appropriate for automation.

# Results

To generate E8 use:

```python
source_values = {
            HDMI1: 0x11,
            HDMI2: 0x12,
            DP1: 0x0F,
            DP2: 0x13,
            USBC: 0x1B,
        }
def model(S2, S3, S4):
    a = source_values[S2] << 0
    b = source_values[S3] << 5
    c = source_values[S4] << 10
    return  a ^ b ^ c # XOR
```

S2, S3, S4 - are window numbers as reported by the monitor's OSD, for example with 2x2 it's: ◰ ◳ ◲ ◱.

# Details

See [analyse_inputs.ipynb].
