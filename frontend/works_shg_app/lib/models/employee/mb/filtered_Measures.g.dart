// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'filtered_Measures.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

_$_FilteredMeasurements _$$_FilteredMeasurementsFromJson(
        Map<String, dynamic> json) =>
    _$_FilteredMeasurements(
      totalSorAmount: (json['totalSorAmount'] as num?)?.toDouble(),
      totalNorSorAmount: (json['totalNorSorAmount'] as num?)?.toDouble(),
      totalAmount: (json['totalAmount'] as num?)?.toDouble(),
      musterRollNumber: json['musterRollNumber'] as String?,
      mbNumber: json['mbNumber'] as String?,
      wfStatus: json['wfStatus'] as String?,
      tenantId: json['tenantId'] as String?,
      measures: (json['measures'] as List<dynamic>?)
          ?.map((e) =>
              FilteredMeasurementsMeasure.fromJson(e as Map<String, dynamic>))
          .toList(),
    );

Map<String, dynamic> _$$_FilteredMeasurementsToJson(
        _$_FilteredMeasurements instance) =>
    <String, dynamic>{
      'totalSorAmount': instance.totalSorAmount,
      'totalNorSorAmount': instance.totalNorSorAmount,
      'totalAmount': instance.totalAmount,
      'musterRollNumber': instance.musterRollNumber,
      'mbNumber': instance.mbNumber,
      'wfStatus': instance.wfStatus,
      'tenantId': instance.tenantId,
      'measures': instance.measures,
    };

_$_FilteredMeasurementsMeasure _$$_FilteredMeasurementsMeasureFromJson(
        Map<String, dynamic> json) =>
    _$_FilteredMeasurementsMeasure(
      length: (json['length'] as num?)?.toDouble(),
      breath: (json['breath'] as num?)?.toDouble(),
      height: (json['height'] as num?)?.toDouble(),
      numItems: (json['numItems'] as num?)?.toDouble(),
      currentValue: (json['currentValue'] as num?)?.toDouble(),
      cumulativeValue: (json['cumulativeValue'] as num?)?.toDouble(),
      tenantId: json['tenantId'] as String?,
      contracts: (json['contracts'] as List<dynamic>?)
          ?.map((e) =>
              FilteredMeasurementsContract.fromJson(e as Map<String, dynamic>))
          .toList(),
    );

Map<String, dynamic> _$$_FilteredMeasurementsMeasureToJson(
        _$_FilteredMeasurementsMeasure instance) =>
    <String, dynamic>{
      'length': instance.length,
      'breath': instance.breath,
      'height': instance.height,
      'numItems': instance.numItems,
      'currentValue': instance.currentValue,
      'cumulativeValue': instance.cumulativeValue,
      'tenantId': instance.tenantId,
      'contracts': instance.contracts,
    };

_$_FilteredMeasurementsContract _$$_FilteredMeasurementsContractFromJson(
        Map<String, dynamic> json) =>
    _$_FilteredMeasurementsContract(
      estimateId: json['estimateId'] as String?,
      estimateLineItemId: json['estimateLineItemId'] as String?,
      contractLineItemRef: json['contractLineItemRef'] as String?,
      unitRate: (json['unitRate'] as num?)?.toDouble(),
      status: json['status'] as String?,
      estimates: (json['estimates'] as List<dynamic>?)
          ?.map((e) =>
              FilteredMeasurementsEstimate.fromJson(e as Map<String, dynamic>))
          .toList(),
    );

Map<String, dynamic> _$$_FilteredMeasurementsContractToJson(
        _$_FilteredMeasurementsContract instance) =>
    <String, dynamic>{
      'estimateId': instance.estimateId,
      'estimateLineItemId': instance.estimateLineItemId,
      'contractLineItemRef': instance.contractLineItemRef,
      'unitRate': instance.unitRate,
      'status': instance.status,
      'estimates': instance.estimates,
    };

_$_FilteredMeasurementsEstimate _$$_FilteredMeasurementsEstimateFromJson(
        Map<String, dynamic> json) =>
    _$_FilteredMeasurementsEstimate(
      id: json['id'] as String?,
      sorId: json['sorId'] as String?,
      category: json['category'] as String?,
      name: json['name'] as String?,
      description: json['description'] as String?,
      unitRate: (json['unitRate'] as num?)?.toDouble(),
      noOfunit: json['noOfunit'] as int?,
      uom: json['uom'] as String?,
      length: json['length'] as int?,
      width: json['width'] as int?,
      height: json['height'] as int?,
      quantity: json['quantity'] as int?,
      isDeduction: json['isDeduction'] as bool?,
    );

Map<String, dynamic> _$$_FilteredMeasurementsEstimateToJson(
        _$_FilteredMeasurementsEstimate instance) =>
    <String, dynamic>{
      'id': instance.id,
      'sorId': instance.sorId,
      'category': instance.category,
      'name': instance.name,
      'description': instance.description,
      'unitRate': instance.unitRate,
      'noOfunit': instance.noOfunit,
      'uom': instance.uom,
      'length': instance.length,
      'width': instance.width,
      'height': instance.height,
      'quantity': instance.quantity,
      'isDeduction': instance.isDeduction,
    };
