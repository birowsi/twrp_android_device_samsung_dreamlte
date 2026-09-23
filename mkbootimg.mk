$(INSTALLED_RECOVERYIMAGE_TARGET): $(recoveryimage-deps) $(DEVICE_PATH)/append_legacy_dt.py $(DEVICE_PATH)/dtb
	$(MKBOOTIMG) $(INTERNAL_RECOVERYIMAGE_ARGS) \
		$(INTERNAL_MKBOOTIMG_VERSION_ARGS) $(BOARD_RECOVERY_MKBOOTIMG_ARGS) \
		--output $@.nodt
	python3 $(DEVICE_PATH)/append_legacy_dt.py $@.nodt $(DEVICE_PATH)/dtb $@
	rm -f $@.nodt
	$(call assert-max-image-size,$@,$(BOARD_RECOVERYIMAGE_PARTITION_SIZE))
