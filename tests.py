from enum import IntEnum
import pytest
from hypothesis import given, strategies as st


class Input(IntEnum):
    HDMI1 = 0x11  # 17
    HDMI2 = 0x12  # 18
    DP1 = 0x0F  # 15
    DP2 = 0x13  # 19
    USBC = 0x1B  # 27


def model_pbp_order(S2: Input, S3: Input, S4: Input) -> int:
    return (S2 << 0) ^ (S3 << 5) ^ (S4 << 10)


def decode_pbp_order(value: int) -> tuple[Input, ...]:
    S2 = Input(value & 0x1F)
    S3 = Input((value >> 5) & 0x1F)
    S4 = Input((value >> 10) & 0x1F)
    return S2, S3, S4


@given(
    st.tuples(
        st.sampled_from(list(Input)),
        st.sampled_from(list(Input)),
        st.sampled_from(list(Input)),
    )
)
def test_model_decode_inverse(inputs: tuple[Input, ...]) -> None:
    S2, S3, S4 = inputs
    encoded = model_pbp_order(S2, S3, S4)
    decoded = decode_pbp_order(encoded)
    assert decoded == (S2, S3, S4)


class KvmUSBIdx(IntEnum):
    USB1 = 1
    USB2 = 2
    USB3 = 3
    USB4 = 4


def model_kvm_inputs(
    DP1: KvmUSBIdx,
    DP2: KvmUSBIdx,
    HDMI1: KvmUSBIdx,
    HDMI2: KvmUSBIdx,
) -> int:
    return (
        ((DP1 - 1) << 12) ^ ((DP2 - 1) << 10) ^ ((HDMI1 - 1) << 8) ^ ((HDMI2 - 1) << 6)
    )


def decode_kvm_inputs(value: int) -> tuple[KvmUSBIdx, ...]:
    DP1 = KvmUSBIdx(((value >> 12) & 0b11) + 1)
    DP2 = KvmUSBIdx(((value >> 10) & 0b11) + 1)
    HDMI1 = KvmUSBIdx(((value >> 8) & 0b11) + 1)
    HDMI2 = KvmUSBIdx(((value >> 6) & 0b11) + 1)
    return DP1, DP2, HDMI1, HDMI2


@given(
    st.tuples(
        st.sampled_from(list(KvmUSBIdx)),
        st.sampled_from(list(KvmUSBIdx)),
        st.sampled_from(list(KvmUSBIdx)),
        st.sampled_from(list(KvmUSBIdx)),
    )
)
def test_decode_kvm_inputs(inputs: tuple[KvmUSBIdx, ...]) -> None:
    DP1, DP2, HDMI1, HDMI2 = inputs
    encoded = model_kvm_inputs(DP1, DP2, HDMI1, HDMI2)
    decoded = decode_kvm_inputs(encoded)
    assert decoded == (DP1, DP2, HDMI1, HDMI2)
