import { Loader, FormComposerV2, Header, Toast, ActionBar, Menu, SubmitBar, WorkflowModal } from "@egovernments/digit-ui-react-components";
import React, { useState, useEffect, useCallback } from "react";
import { useTranslation } from "react-i18next";
import { useHistory } from "react-router-dom";
import { CreateConfig } from "../../configs/RateAnalysisCreateConfig";
import { getDefaultValues } from "../../utils/transformData";
import getModalConfig from "../../../../Measurement/src/pages/employee/config";
import { deepCompare } from "../../utils/transformData";
import _ from "lodash";

const updateData = (data, formState, tenantId) => {
  const SOR = data?.SORtable || formState?.SOR;
  const NONSOR = data?.NONSORtable || formState?.NONSOR;
  return { ...formState, ...data, SOR, NONSOR, tenantId };
};

const CreateRateAnalysis = ({ props }) => {
  const tenantId = Digit.ULBService.getCurrentTenantId();
  const { t } = useTranslation();
  const history = useHistory();
  const rolesForThisAction = "MUKTA_STATE_ADMIN"; 
  //const MeasurementSession = Digit.Hooks.useSessionStorage("MEASUREMENT_CREATE", {});
  const queryStrings = Digit.Hooks.useQueryParams();
  // const [sessionFormData, setSessionFormData, clearSessionFormData] = MeasurementSession;
  const [createState, setState] = useState({ SORDetails:[], extraCharges:[], accessors: undefined, period: {} });
  const [defaultState, setDefaultState] = useState({ SORDetails:[], extraCharges:[] });
  const [showToast, setShowToast] = useState({display: false, error: false});
  const [errorMessage, setErrorMessage] = useState("");
  const [displayMenu, setDisplayMenu] = useState(false);
  const [config, setConfig] = useState({});
  const [approvers, setApprovers] = useState([]);
  const [showModal, setShowModal] = useState(false);
  const [selectedApprover, setSelectedApprover] = useState({});


  const getFormAccessors = useCallback((accessors) => {
    if (!createState?.accessors) {
      setState((old) => ({ ...old, accessors }));
    }
  }, []);
  // get contractNumber from the url
  const searchparams = new URLSearchParams(location.search);
  const contractNumber = searchparams.get("workOrderNumber");
  const mbNumber = searchparams.get("mbNumber");

  // use this for call create or update
  // const reqCriteria = {
  //   url: props?.isUpdate ? `/measurement-service/v1/_update` : `/measurement-service/v1/_create`,
  //   params: {},
  //   body: {},
  //   config: {
  //     enabled: false,
  //   },
  // };

  // const mutation = Digit.Hooks.useCustomAPIMutationHook(reqCriteria);

  // for MDMS service
  const requestCriteria = {
    url: "/mdms-v2/v2/_search",
    body: {
    MdmsCriteria: {
        tenantId: tenantId,
        // moduleDetails: [
        // {
        //     moduleName: "WORKS-SOR",
        //     masterDetails: [
        //     {
        //         name: "SOR",
        //         filter: `[?(@.sorId=='${queryStrings?.sorid}')]`,
        //     },
        //     ],
        // },
        // ],
        schemaCode: "WORKS-SOR.SOR",
        uniqueIdentifiers : [`${queryStrings?.sorid}`],
    },
    },
    changeQueryName:"sorRates"
};

const { isLoading, data : data} = Digit.Hooks.useCustomAPIHook(requestCriteria);

  const { isLoading: approverLoading, isError, error, data: employeeDatav1 } = Digit.Hooks.hrms.useHRMSSearch(
    { roles: rolesForThisAction, isActive: true },
    Digit.ULBService.getCurrentTenantId(),
    null,
    null,
    { enabled: true }
  );

  employeeDatav1?.Employees.map((emp) => (emp.nameOfEmp = emp?.user?.name || "NA"));

  

  // fetch the required data........
  useEffect(() => {
    const fetchRequiredData = () => {
      if (data) {
        const defaultValues = getDefaultValues(data?.mdms?.[0], t, mbNumber);
        setState({
          //SOR: defaultValues?.SOR,
          //NONSOR: defaultValues?.NONSOR,
          //SORtable : defaultValues?.SOR,
          //NONSORtable: defaultValues?.NONSOR,
          SORDetails : [],
          ...defaultValues?.SORData,
          extraCharges:[],
          //period: data?.period,
          //musterRollNumber: data?.musterRollNumber,
          //uploadedDocs: defaultValues?.uploadedDocs,
          //documents : defaultValues?.documents,
        });
        setDefaultState({
          //SOR: defaultValues?.SOR,
          //NONSOR: defaultValues?.NONSOR,
          //SORtable : defaultValues?.SOR,
          //NONSORtable: defaultValues?.NONSOR,
          SORDetails : [],
          sordata: data?.mdms?.[0],
          extraCharges:[],
          //estimate: data?.estimate,
          //contractDetails: defaultValues?.contractDetails,
          //uploadedDocs: defaultValues?.uploadedDocs,
          //documents : defaultValues?.documents,
        });
        //createState?.accessors?.setValue?.("SOR", defaultValues?.SOR);
        //createState?.accessors?.setValue?.("NONSOR", defaultValues?.NONSOR);
        createState?.accessors?.setValue?.("SORDetails", []);
        createState?.accessors?.setValue?.("extraCharges", []);
        createState?.accessors?.setValue?.("sordata", data?.mdms?.[0]);
        if (data?.period?.type == "error") {
          setErrorMessage(data?.period?.message);
          setShowToast({display:true, error:true});
        }
      }
    };
    fetchRequiredData();
  }, [data]);

  useEffect(() => {
    setApprovers(employeeDatav1?.Employees?.length > 0 ? employeeDatav1?.Employees.filter((emp) => emp?.nameOfEmp !== "NA") : []);
  }, [employeeDatav1]);
  useEffect(() => {
    setConfig(
      getModalConfig({
        t,
        approvers,
        selectedApprover,
        setSelectedApprover,
        approverLoading,
        isEdit : props?.isUpdate,
      })
    );
  }, [approvers]);

  // action to be performed....
  let actionMB = [
    {
      name: "SUBMIT",
    },
    {
      name: "SAVE_AS_DRAFT",
    },
  ];

  function onActionSelect(action = "SUBMIT") {
    if (createState?.period?.type == "error") {
      setErrorMessage(createState?.period?.message);
      setShowToast({display:true, error:true});
      return null;
    }
    if (action?.name === "SUBMIT") {
      createState.workflowAction = "SUBMIT";
      setShowModal(true);
      //handleCreateMeasurement(createState, action);
    }
    if (action?.name === "SAVE_AS_DRAFT") {
      createState.workflowAction = "SAVE_AS_DRAFT";
      handleCreateRateAnalysis(createState, action);
    }
  }

  // Handle form submission
  const handleCreateRateAnalysis = async (data, action) => {
    setShowModal(false);
    if (props?.isUpdate) {
      data.id = props?.data?.[0].id;
      data.measurementNumber = props?.data?.[0].measurementNumber;
      data.wfStatus = props?.data?.[0]?.wfStatus;
    }

    if(selectedApprover)
      data.selectedApprover = selectedApprover;
    // Create the measurement payload with transformed data
    const measurements = transformData(updateData(data, createState, tenantId));
    //call the createMutation for MB and route to response page on onSuccess or show error
    const onError = (resp) => {
      setErrorMessage(resp?.response?.data?.Errors?.[0]?.message);
      setShowToast({display:true, error:true});
    };
    const onSuccess = (resp) => {
      if(action?.name === "SAVE_AS_DRAFT")
      {
        setErrorMessage(t("MB_APPLICATION_IS_SUCCESSFULLY_DRAFTED"));
        setShowToast({display:true, error:false});
        setTimeout(() => {history.push(`/${window.contextPath}/employee/measurement/update?tenantId=${resp.measurements[0].tenantId}&workOrderNumber=${contractNumber}&mbNumber=${resp.measurements[0].measurementNumber}`)}, 3000);;
      }
      else
        history.push(`/${window.contextPath}/employee/measurement/response?mbreference=${resp.measurements[0].measurementNumber}`);
    };
    mutation.mutate(
      {
        params: {},
        body: { ...measurements },
        config: {
          enabled: true,
        },
      },
      {
        onError,
        onSuccess,
      }
    );
  };

  const closeToast = () => {
    setShowToast({display:false, error:false});;
  };
  //remove Toast after 3s
  useEffect(() => {
    if (showToast) {
      setTimeout(() => {
        closeToast();
      }, 3000);
    }
  }, [showToast]);

  // useEffect(() => {
  //   if (!_.isEqual(sessionFormData, createState)) {
  //     // setSessionFormData({ ...createState });
  //   }
  //   console.log(createState,"formdata",sessionFormData)
  // }, [createState]);

  const onFormValueChange = (setValue, formData, formState, reset, setError, clearErrors, trigger, getValues) => {
    if (deepCompare(formData,createState)) {
      setState({ ...createState, ...formData })
    }
  };
  actionMB = actionMB && (props?.isUpdate) && props?.data && props?.data?.[0]?.wfStatus==="SENT_BACK" ? actionMB?.filter((ob) => ob?.name !== "SAVE_AS_DRAFT") : actionMB;

  // if data is still loading return loader
  if (isLoading || !defaultState?.sordata || approverLoading) {
    return <Loader />;
  }

  // else render form and data
  return (
    <div>
      {showModal && <WorkflowModal closeModal={() => setShowModal(false)} onSubmit={(_data) => handleCreateRateAnalysis({..._data,...createState},"SUBMIT")} config={config} />}
      <Header className="works-header-view modify-header">{t("RA_CREATE_RATE_ANALYSIS")}</Header>
      <FormComposerV2
        label={t("MB_SUBMIT_BAR")}
        config={CreateConfig({ defaultValue: defaultState?.sordata, measurement : props?.data[0] }).CreateConfig[0]?.form?.filter((a) => (!a.hasOwnProperty('forOnlyUpdate') || props?.isUpdate)).map((config) => {
          return {
            ...config,
            body: config.body.filter((a) => !a.hideInEmployee),
          };
        })}
        getFormAccessors={getFormAccessors}
        defaultValues={{ ...createState }}
        onSubmit={onActionSelect}
        fieldStyle={{ marginRight: 0 }}
        showMultipleCardsWithoutNavs={true}
        onFormValueChange={onFormValueChange}
        noBreakLine={true}
      />
      {showToast?.display && <Toast error={showToast?.error} label={errorMessage} isDleteBtn={true} onClose={closeToast} />}
      <ActionBar>
        {displayMenu ? <Menu localeKeyPrefix={"WF"} options={actionMB} optionKey={"name"} t={t} onSelect={onActionSelect} /> : null}
        <SubmitBar label={t("ACTIONS")} onSubmit={() => setDisplayMenu(!displayMenu)} />
      </ActionBar>
    </div>
  );
};
export default CreateRateAnalysis;
