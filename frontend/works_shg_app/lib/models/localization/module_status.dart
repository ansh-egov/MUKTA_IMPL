// ignore_for_file: invalid_annotation_target

import 'package:freezed_annotation/freezed_annotation.dart';

part 'module_status.freezed.dart';
part 'module_status.g.dart';

@freezed
class ModuleStatus with _$ModuleStatus {

   factory ModuleStatus({
    required bool isEng,
    required String label,
    required String value,
    required bool isOdia,
  }) = _ModuleStatus;

  factory ModuleStatus.fromJson(Map<String, dynamic> json) =>
      _$ModuleStatusFromJson(json);
}

