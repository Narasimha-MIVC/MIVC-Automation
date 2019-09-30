__author__ = "nitin.kumar-2@mitel.com"

import sys, requests, os, logging, ast, json
from prg_btns_constants import function_ids
sys.path.append(os.path.normpath(os.path.dirname(os.path.dirname(os.path.dirname((__file__))))))
from utils.decorators import func_logger

log = logging.getLogger("boss_api.prog_buttons")


class ProgButtons():
    """
    Apis for the programmable buttons related operations.
    """

    @func_logger
    def configure_prog_button(self, **params):
        '''
        This function will configure a programmable button on the phone
        Users -> select a user -> click on second coloum -> Programmable Buttons
        user_email : the email of the user
        button_box : the number of button box generally always is 0
        soft_key : the index of soft key in btn box list e.g. for the button 2 on the boss ui the value of soft_key should be 1 i.e. decremented by 1
        :return: A tuple of a boolean status flag and the return object from the requested url
        '''
        result = False
        params_xml = self.config.getparams("configure_prog_button")
        params = self.get_param_to_use(params_xml, **params)
        if self.accountId is None:  # switch account has not been called
            act_id = self.get_account_detail(act_name=params['account_name'])
        else:
            act_id = self.accountId
        params["accountId"] = act_id
        params["profileId"] = self.get_profile_detail(act_id, params['part_name'],params['user_email'])
        # get programmable btns data

        prg_btn_data = self.get_programmable_btns_data(act_id, params["profileId"])

        # button boxes
        btn_box = "user_prog_button_button_%s_boxes_attributes"%params['button_box']
        prg_btn_data["user"][btn_box][params['soft_key']]['selectedFunction'] = params["function"]
        prg_btn_data["user"][btn_box][params['soft_key']]['SoftKeyLabel'] = params["label"][0:6]
        prg_btn_data["user"][btn_box][params['soft_key']]['LongLabel'] = params["label"][0:12]
        prg_btn_data["user"][btn_box][params['soft_key']]['DialNumberDN_formatted'] = params["extension"]
        prg_btn_data["user"][btn_box][params['soft_key']]['ConnectedCallFunctionID'] = None
        prg_btn_data["user"][btn_box][params['soft_key']]['_create'] = True
        prg_btn_data["user"][btn_box][params['soft_key']]['FunctionID'] = function_ids[params["function"].replace(" ","_").upper()]
        prg_btn_data["user"][btn_box][params['soft_key']]['DialNumberNTID'] = "0"

        url = params.pop("url")
        log.info("configuring a programmable button on the phone with args <%s>" % params)
        # changing the content type for this call
        self.headers['Content-Type'] = "application/json"
        ret = requests.post(url, data=json.dumps(prg_btn_data), headers=self.headers, params=params)
        # changing the content type back to default for further calls
        self.headers['Content-Type'] = "application/x-www-form-urlencoded"

        if ret.status_code == 200 and not ret.json().has_key("errors"):
            log.info("The programmable button has been created successfully.Message from server : <%s>" % ret.text)
            result = True
        else:
            log.error("Could not create programmable button.Message from server : <%s>" % ret.text)

        return result, ret

    @func_logger
    def clear_prog_button(self, **params):
        '''
        This function will clear all the onfigured  programmable buttons
        Users -> select a user -> click on second coloum -> Programmable Buttons
        user_email : the email of the user
        button_box : the number of button box generally always is 0
        soft_key : the index of soft key in btn box list e.g. for the button 2 on the boss ui the value of soft_key should be 1 i.e. decremented by 1
        :return: A tuple of a boolean status flag and the return object from the requested url
        '''
        result = False
        params_xml = self.config.getparams("configure_prog_button")
        params = self.get_param_to_use(params_xml, **params)
        if self.accountId is None:  # switch account has not been called
            act_id = self.get_account_detail(act_name=params['account_name'])
        else:
            act_id = self.accountId
        params["accountId"] = act_id
        params["profileId"] = self.get_profile_detail(act_id, params['part_name'], params['user_email'])

        # get programmable btns data
        prg_btn_data = self.get_programmable_btns_data(act_id, params["profileId"])
        # button boxes
        btn_box = "user_prog_button_button_%s_boxes_attributes"%params['button_box']
        prg_btn_data["user"][btn_box][params['soft_key']]['FunctionID'] = 2
        prg_btn_data["user"][btn_box][params['soft_key']]['DialNumberNTID'] = -1
        prg_btn_data["user"][btn_box][params['soft_key']]['DialNumberExtern_formatted'] = ""
        prg_btn_data["user"][btn_box][params['soft_key']]['DialNumberDN_formatted'] = ""

        url = params.pop("url")
        log.info("clearing the configured programmable button on the phone with args <%s>" % params)
        self.headers['Content-Type'] = "application/json"
        ret = requests.post(url, data=json.dumps(prg_btn_data), headers=self.headers, params=params)

        # removing extra check as trying to remove a btn which is already removed raises an exception
        if ret.status_code == 200 :
            log.info("The programmable buttons have been cleared successfully.")
            result = True
        else:
            log.error("Could not clear programmable buttons.Message from server : <%s>" % ret.text)

        return result, ret

