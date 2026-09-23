# TWRP for Samsung Galaxy S8

TWRP `3.7.1_12` device tree for the Exynos Galaxy S8 (`dreamlte`), tested on the
Korean SM-G950N.

## Downloads

Use the IMG file when flashing from an existing recovery. Use the IMG TAR with
the AP slot in Odin.

The release is intentionally named `3.7.1_12-0`; it does not contain Miku UI
branding. The Miku UI ROM ships its own `3.7.1_12-miku` build.

## Tested

- Recovery boot and touch input
- Display brightness and vibration
- Battery percentage and charging status
- Internal storage and `/data/media`
- ADB
- Windows MTP in both directions
- NTFS, exFAT and F2FS support
- SELinux Enforcing

MTP and ADB were tested with matching SHA-256 hashes after bidirectional file
transfers. The battery reading uses TWRP's legacy battery service because the
Android 12 recovery health service does not report this device correctly.

## Flashing

### Existing recovery

1. Select **Install Image**.
2. Choose `twrp-3.7.1_12-0-dreamlte.img`.
3. Select the **Recovery** partition.
4. Flash and reboot directly back to recovery once.

### Odin

1. Boot the phone into Download Mode.
2. Load `twrp-3.7.1_12-0-dreamlte.img.tar` in the **AP** slot.
3. Disable **Auto Reboot**.
4. Flash, then boot directly into recovery with the hardware keys.

Flashing custom recovery trips Knox. Keep an EFS backup before modifying the
phone.

## Building

```bash
mkdir -p ~/twrp
cd ~/twrp

repo init \
  -u https://github.com/minimal-manifest-twrp/platform_manifest_twrp_aosp.git \
  -b twrp-12.1
repo sync -c -j$(nproc)

git clone -b android-12.1 \
  https://github.com/birowsi/twrp_android_device_samsung_dreamlte.git \
  device/samsung/dreamlte

git -C bootable/recovery apply \
  ../../device/samsung/dreamlte/patches/twrp-12.1/0001-data-media-selinux.patch
git -C bootable/recovery apply \
  ../../device/samsung/dreamlte/patches/twrp-12.1/0002-mtp-reopen.patch

export ALLOW_MISSING_DEPENDENCIES=true
source build/envsetup.sh
lunch twrp_dreamlte-eng
mka recoveryimage
```

The image is written to `out/target/product/dreamlte/recovery.img`.

## Technical notes

The Exynos 8895 bootloader uses the legacy Android boot image DT section. The
tree builds the standard TWRP ramdisk, creates a legacy recovery image with the
official kernel and DT payload, and checks that the result fits the
48,234,496-byte recovery partition.

The two recovery patches restore the `/data/media` SELinux context after a data
format and reopen the FunctionFS MTP descriptor when the USB service restarts.

## Credits

TeamWin, LineageOS, corsicanu and the Android Open Source Project.
