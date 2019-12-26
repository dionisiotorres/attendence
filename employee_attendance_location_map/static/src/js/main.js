 odoo.define('employee_attendance_location_map.main', function (require) {
"use strict";
    
var hr_attendance = require('hr_attendance.my_attendances');
var KioskMode = require('hr_attendance.kiosk_confirm');

    hr_attendance.include({
        update_attendance: function () {
             var self = this;
             if ("geolocation" in navigator){
                navigator.permissions.query({name:'geolocation'}).then(function(result) {
                    // result.state Will return ['granted', 'prompt', 'denied']
                    if (result.state != 'denied'){
                        navigator.geolocation.getCurrentPosition(function(position) {
                            self.attendance_check(position.coords.latitude, position.coords.longitude);
                        });
                    } else {
                        self.attendance_check('', '');
                    }
                });
            } else {
                self.attendance_check('', '');
            }
        },

        attendance_check: function (latitude, longitude) {
            var self = this;
                self._rpc({
                    model: 'hr.employee',
                    method: 'attendance_manual',
                    args: [[self.employee.id], 'hr_attendance.hr_attendance_action_my_attendances','',latitude,longitude],
                    })
                    .then(function(result) {
                        if (result.action) {
                            self.do_action(result.action);
                        } else if (result.warning) {
                            self.do_warn(result.warning);
                        }
                    });
        },
    });

    KioskMode.include({
        events: _.extend({}, KioskMode.prototype.events, {
            "click .o_hr_attendance_sign_in_out_icon": function () {
                var self = this;
                if ("geolocation" in navigator){
                    navigator.geolocation.getCurrentPosition(function(position) {
                        self._rpc({
                            model: 'hr.employee',
                            method: 'attendance_manual',
                            args: [[self.employee_id], self.next_action,'',position.coords.latitude,position.coords.longitude],
                        })
                            .then(function(result) {
                                if (result.action) {
                                    self.do_action(result.action);
                                } else if (result.warning) {
                                    self.do_warn(result.warning);
                                    self.$('.o_hr_attendance_sign_in_out_icon').removeAttr("disabled");
                                }
                            });

                    });
                }
                this.$('.o_hr_attendance_sign_in_out_icon').attr("disabled", "disabled");
            },
        }),

    });
});