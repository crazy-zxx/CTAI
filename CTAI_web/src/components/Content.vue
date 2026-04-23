<template>
    <div id="Content">
        <el-dialog
            id="hello"
            title="肿瘤辅助诊断系统使用须知"
            :visible.sync="centerDialogVisible"
            width="65%"
            :before-close="handleClose"
        >
            <el-steps :active="5" finish-status="process ">
                <el-step title="步骤1" style="width:280px;padding-left: 50px">
                    <template slot="description">
                        <p style="font-size: 16px">下载测试CT文件文件</p>
                        <br>
                        <br>
                    </template>
                </el-step>
                <el-step title="步骤2" style="width:260px;margin-left:-5px;">
                    <template slot="description">
                        <p>上传CT图像至服务器</p>
                        <p>使用训练的模型预测肿瘤区域</p>
                        <p>并返回肿瘤区域特征</p>
                    </template>
                </el-step>
                <el-step title="步骤3" style="width:260px;margin-left:-5px;">
                    <template slot="description">
                        <div>
                            <p>根据预测的肿瘤区域和特征</p>
                            <p>进行辅助诊断</p>
                            <br>
                        </div>
                    </template>
                </el-step>
            </el-steps>
            <span slot="footer" class="dialog-footer">
        <el-button type="primary" @click="welcome">下载测试CT图像</el-button>
      </span>
        </el-dialog>
        <el-dialog
            title="AI预测中"
            :visible.sync="dialogTableVisible"
            :show-close="false"
            :close-on-press-escape="false"
            :append-to-body="true"
            :close-on-click-modal="false"
            :center="true"
        >
            <el-progress :percentage="percentage"></el-progress>
            <span slot="footer" class="dialog-footer">非GPU学生服务器性能有限，请耐心等待约一分钟</span>
        </el-dialog>

        <div id="aside">
            <!-- 病人信息输入 -->
            <el-card class="box-card" style="width:250px;height:550px">
                <div slot="header" class="clearfix">
                    <span>病人信息</span>
                </div>
                <el-form :model="patient" label-width="80px" class="patient-form">
                    <el-form-item label="患者ID">
                        <el-input v-model="patient.patient_id" placeholder="请输入患者ID"></el-input>
                    </el-form-item>
                    <el-form-item label="姓名">
                        <el-input v-model="patient.name" placeholder="请输入姓名"></el-input>
                    </el-form-item>
                    <el-form-item label="性别">
                        <el-select v-model="patient.gender" placeholder="请选择性别">
                            <el-option label="男" value="男"></el-option>
                            <el-option label="女" value="女"></el-option>
                        </el-select>
                    </el-form-item>
                    <el-form-item label="年龄">
                        <el-input v-model.number="patient.age" placeholder="请输入年龄"></el-input>
                    </el-form-item>
                    <el-form-item label="电话">
                        <el-input v-model="patient.phone" placeholder="请输入电话"></el-input>
                    </el-form-item>
                    <el-form-item label="部位">
                        <el-input v-model="patient.body_part" placeholder="请输入部位"></el-input>
                    </el-form-item>
                    <el-form-item>
                        <el-button type="primary" @click="loadPatientInfo">加载患者信息</el-button>
                    </el-form-item>
                </el-form>
            </el-card>

            <!-- 步骤条：下载 上传 -->
            <el-card
                class="box-card"
                body-style="padding: 15px 5px 15px 10px"
                style="width:250px;height:500px;margin-top:50px;"
            >
                <div slot="header" class="clearfix" style="text-align:center;">
                    <span class="steps" style="letter-spacing: 7px;">诊断测试步骤</span>
                </div>
                <div style="height: 600px;" class="step_1">
                    <el-steps direction="vertical" :active="active" finish-status="success">
                        <el-step style="height: 120px;" title="步骤 1">
                            <template slot="description" style="font-size: 10px!important;">
                                下载测试CT文件
                                <!-- 下载文件 -->
                                <el-button
                                    type="primary"
                                    icon="el-icon-download"
                                    @click="downTemplate"
                                    class="download_bt"
                                >下载
                                </el-button>
                            </template>
                        </el-step>
                        <el-step style="height: 150px;" title="步骤 2">
                            <template slot="description">
                                <!-- 上传文件 -->
                                上传CT图像至服务器，使用训练的模型预测肿瘤区域并返回肿瘤区域特征
                                <el-button type="primary" icon="el-icon-upload" class="download_bt">上传</el-button>
                                <input class="file" name="file" type="file" @change="update">
                            </template>
                        </el-step>

                        <!-- 获得图像 -->
                        <el-step title="获得图像及特征" style="height: 200px;">
                            <template slot="description"></template>
                        </el-step>
                    </el-steps>
                </div>
            </el-card>
        </div>
        <!-- 上传返回信息部分：原CT图部分  标出肿瘤的CT图像 图像特征-->
        <div id="CT">
            <!-- CT图像 -->
            <div id="CT_image">
                <!-- 原CT图 -->
                <el-card
                    id="CT_image_1"
                    class="box-card"
                    style="border-radius: 8px;width:800px;height:360px;margin-bottom:-30px;"
                >
                    <div class="demo-image__preview1">
                        <div
                            v-loading="loading"
                            element-loading-text="上传图片中"
                            element-loading-spinner="el-icon-loading"
                        >
                            <el-image
                                :src="url_1"
                                class="image_1"
                                :preview-src-list="srcList"
                                style="border-radius: 3px 3px 0 0"
                            >
                                <div slot="error">
                                    <div slot="placeholder" class="error">
                                        <el-button
                                            v-show="showbutton"
                                            type="primary"
                                            icon="el-icon-upload"
                                            class="download_bt"
                                            v-on:click="true_upload"
                                        >
                                            上传dcm文件
                                            <input
                                                ref="upload"
                                                style="display: none"
                                                name="file"
                                                type="file"
                                                @change="update"
                                            >
                                        </el-button>
                                    </div>
                                </div>
                            </el-image>
                        </div>
                        <!-- 原CT图文字 -->
                        <div class="img_info_1" style="border-radius:0 0 5px 5px;">
                            <span style="color:white;letter-spacing:6px;">原CT图像</span>
                        </div>
                    </div>
                    <!-- 标出肿瘤的CT图像 -->
                    <div class="demo-image__preview2">
                        <div
                            v-loading="loading"
                            element-loading-text="处理中,请耐心等待"
                            element-loading-spinner="el-icon-loading"
                        >
                            <el-image
                                :src="url_2"
                                class="image_1"
                                :preview-src-list="srcList1"
                                style="border-radius: 3px 3px 0 0;"
                            >
                                <div slot="error">
                                    <div slot="placeholder" class="error">{{wait_return}}</div>
                                </div>
                            </el-image>
                        </div>
                        <!-- 标出肿瘤的CT图像文字 -->
                        <div class="img_info_1" style="border-radius: 0 0 5px 5px;">
                            <span style="color:white;letter-spacing:4px;">标出肿瘤的CT图像</span>
                        </div>
                    </div>
                </el-card>
            </div>


            <!-- 分割线 -->

            <!-- 图像特征部分 -->
            <div id="info_patient">
                <!-- 卡片放置表格 -->
                <el-card style="border-radius: 8px;">
                    <div slot="header" class="clearfix">
                        <span>肿瘤区域特征值</span>
                        <el-button
                            style="margin-left: 35px"
                            v-show="!showbutton"
                            type="primary"
                            icon="el-icon-upload"
                            class="download_bt"
                            v-on:click="true_upload2"
                        >
                            重新选择图像
                            <input
                                ref="upload2"
                                style="display: none"
                                name="file"
                                type="file"
                                @change="update"
                            >
                        </el-button>
                    </div>


                    <el-tabs v-model="activeName" @tab-click="handleClick">
                        <el-tab-pane label="肿瘤区域特征值" name="first">
                            <!-- 表格存放特征值 -->
                            <el-table
                                :data="feature_list"
                                height="540"
                                border
                                style="width:750px;text-align:center;"
                                v-loading="loading"
                                element-loading-text="数据正在处理中，请耐心等待"
                                element-loading-spinner="el-icon-loading"
                                lazy
                            >
                                <el-table-column label="Feature" width="250px">
                                    <template slot-scope="scope">
                                        <span>{{scope.row[2]}}</span>
                                    </template>
                                </el-table-column>
                                <!-- 特征名 -->
                                <el-table-column label="特征名" width="250px">
                                    <template slot-scope="scope">
                                        <span>{{scope.row[0]}}</span>
                                    </template>
                                </el-table-column>

                                <!-- 特征值 -->
                                <el-table-column label="特征值" width="250px">
                                    <template slot-scope="scope">
                                        <span>{{scope.row[1]}}</span>
                                    </template>
                                </el-table-column>
                            </el-table>
                        </el-tab-pane>
                        <el-tab-pane label="面积对比" name="second" style="width:750px;height:540px;">
                            <div id="areaCompare">
                                <el-table

                                    :data="feature_list"
                                    height="540"
                                    border
                                    style="width:750px;text-align:center;"
                                    v-loading="loading"
                                    element-loading-text="数据正在处理中，请耐心等待"
                                    element-loading-spinner="el-icon-loading"
                                >
                                    <el-table-column label="Feature" width="250px">
                                        <template slot-scope="scope">
                                            <span>{{scope.row[2]}}</span>
                                        </template>
                                    </el-table-column>
                                    <!-- 特征名 -->
                                    <el-table-column label="特征名" width="250px">
                                        <template slot-scope="scope">
                                            <span>{{scope.row[0]}}</span>
                                        </template>
                                    </el-table-column>

                                    <!-- 特征值 -->
                                    <el-table-column label="特征值" width="250px">
                                        <template slot-scope="scope">
                                            <span>{{scope.row[1]}}</span>
                                        </template>
                                    </el-table-column>
                                </el-table>
                            </div>
                            <div id="area" style="width: 750px;height:540px;margin-bottom:20px;"></div>
                        </el-tab-pane>
                        <el-tab-pane label="周长对比" name="third" style="width:750px;height:540px;">
                            <div id="perimeterCompare">
                                <el-table

                                    :data="feature_list"
                                    height="540"
                                    border
                                    style="width:750px;text-align:center;"
                                    v-loading="loading"
                                    element-loading-text="数据正在处理中，请耐心等待"
                                    element-loading-spinner="el-icon-loading"
                                >
                                    <el-table-column label="Feature" width="250px">
                                        <template slot-scope="scope">
                                            <span>{{scope.row[2]}}</span>
                                        </template>
                                    </el-table-column>
                                    <!-- 特征名 -->
                                    <el-table-column label="特征名" width="250px">
                                        <template slot-scope="scope">
                                            <span>{{scope.row[0]}}</span>
                                        </template>
                                    </el-table-column>

                                    <!-- 特征值 -->
                                    <el-table-column label="特征值" width="250px">
                                        <template slot-scope="scope">
                                            <span>{{scope.row[1]}}</span>
                                        </template>
                                    </el-table-column>
                                </el-table>
                            </div>

                            <div id="perimeter" style="width: 750px;height:540px;margin-bottom:20px;"></div>
                        </el-tab-pane>
                        <el-tab-pane label="AI辅助诊断" name="fourth" style="width:750px;height:540px;">
                            <!-- AI辅助诊断设置 -->
                            <el-card style="margin-bottom: 20px;" v-if="showAiSettings">
                                <div slot="header" class="clearfix">
                                    <span>AI模型设置</span>
                                </div>
                                <el-form :model="aiSettings" label-width="120px" class="ai-settings-form">
                                    <el-form-item label="API地址">
                                        <el-input v-model="aiSettings.apiUrl" placeholder="请输入API地址"></el-input>
                                    </el-form-item>
                                    <el-form-item label="API密钥">
                                        <el-input v-model="aiSettings.apiKey" type="password" placeholder="请输入API密钥"></el-input>
                                    </el-form-item>
                                    <el-form-item label="模型名称">
                                        <el-input v-model="aiSettings.modelName" placeholder="请输入模型名称"></el-input>
                                    </el-form-item>
                                    <el-form-item>
                                            <el-button type="primary" @click="testModelConnection" style="margin-right: 10px;">测试模型连通性</el-button>
                                            <el-button type="success" @click="saveAiSettingsManually">保存设置</el-button>
                                        </el-form-item>
                                </el-form>
                            </el-card>

                            <!-- AI辅助诊断对话 -->
                            <el-card>
                                <div slot="header" class="clearfix">
                                    <span>AI诊断分析</span>
                                    <div style="float: right;">
                                        <el-button type="text" @click="toggleAiSettings" size="small" style="margin-right: 10px;">
                                            <i class="el-icon-setting"></i>
                                        </el-button>
                                        <el-button type="primary" @click="analyzeWithAI" size="small" style="margin-right: 10px;">开始智能分析</el-button>
                                        <el-button type="danger" @click="resetConversation" size="small">重置对话</el-button>
                                    </div>
                                </div>
                                <div class="ai-chat-container" style="height: 420px; overflow-y: auto;">
                                    <div v-for="(message, index) in aiMessages" :key="index" :class="['ai-message', message.type === 'user' ? 'user-message' : 'ai-message']">
                                        <div class="message-header">
                                            <span>{{ message.type === 'user' ? '用户' : 'AI' }}</span>
                                            <span style="float: right;">{{ message.timestamp }}</span>
                                        </div>
                                        <div class="message-content" v-html="formatAiResponse(message.displayContent || message.content)"></div>
                                        <div v-if="message.loading" class="loading-indicator">
                                            <span>.</span><span>.</span><span>.</span>
                                        </div>
                                    </div>
                                </div>
                            </el-card>
                        </el-tab-pane>
                    </el-tabs>
                </el-card>
            </div>
        </div>
    </div>
</template>

<script>
    import axios from "axios";

    export default {
        name: "Content",
        data() {
            return {
                server_url:'http://127.0.0.1:5003',
                perimeter_picture_data: 0,
                area_picture_data: 0,
                activeName: "first",
                active: 0,
                centerDialogVisible: true,
                url_1: "",
                url_2: "",
                textarea: "",
                srcList: [],
                srcList1: [],
                feature_list: [],
                feature_list_1: [],
                feat_list: [],
                url: "",
                visible: false,
                activeName: "second",
                wait_return: "等待上传",
                wait_upload: "等待上传",
                loading: false,
                table: false,
                isNav: false,
                showbutton: true,
                percentage: 0,
                fullscreenLoading: false,
                opacitys: {
                    opacity: 0
                },
                dialogTableVisible: false,
                patient: {
                    patient_id: "",
                    name: "",
                    gender: "",
                    age: null,
                    phone: "",
                    body_part: ""
                },
                aiSettings: {
                    apiUrl: "",
                    apiKey: "",
                    modelName: ""
                },
                aiMessages: [],
                showAiSettings: false
            };
        },
        created: function () {
            document.title = '肿瘤辅助诊断系统';
            // 从localStorage读取AI设置配置
            this.loadAiSettings();
        },
        watch: {
            // 监听aiSettings变化，自动保存到localStorage
            aiSettings: {
                handler: function(newSettings) {
                    this.saveAiSettings(newSettings);
                },
                deep: true
            }
        },
        methods: {
            true_upload() {
                this.$refs.upload.click();
            },
            true_upload2() {
                this.$refs.upload2.click();
            },
            // handleClose(done) {
            //     this.$confirm("确认关闭？")
            //         .then(_ => {
            //             done();
            //         })
            //         .catch(_ => {
            //         });
            // },
            next() {
                this.active++;
            },
            // 获得目标文件
            getObjectURL(file) {
                var url = null;
                if (window.createObjcectURL != undefined) {
                    url = window.createOjcectURL(file);
                } else if (window.URL != undefined) {
                    url = window.URL.createObjectURL(file);
                } else if (window.webkitURL != undefined) {
                    url = window.webkitURL.createObjectURL(file);
                }
                return url;
            },
            // 点击切换
            handleClick(tab, event) {
                if (tab.name == "second") {
                    this.loadHistoryDiagnoses();
                    this.drawChart();
                    var myChart_area = this.$echarts.init(document.getElementById('area'));
                    myChart_area.setOption({
                        xAxis: {
                            type: "category",
                            data: ["1", "2", "3", "4", "5", "6", "7", "8"]
                        },
                        yAxis: {
                            type: "value",
                            name: "面积"
                        },
                        areaStyle: {},
                        legend: {
                            data: [""]
                        },
                        series: [
                            {
                                name: "面积",
                                type: "line",
                                data: [
                                    1300,
                                    1290,
                                    1272,
                                    1123.5,
                                    1123,
                                    1092,
                                    1086,
                                    this.area_picture_data
                                ]
                            }
                        ]
                    });
                } else if (tab.name == "third") {
                    this.loadHistoryDiagnoses();
                    this.drawChart();
                    var myChart_perimeter = this.$echarts.init(document.getElementById('perimeter'));
                    myChart_perimeter.setOption({
                        xAxis: {
                            type: "category",
                            data: ["1", "2", "3", "4", "5", "6", "7", "8"]
                        },
                        yAxis: {
                            type: "value",
                            name: "周长"
                        },
                        areaStyle: {},
                        series: [
                            {
                                name: "周长",
                                type: "line",
                                data: [
                                    250,
                                    243,
                                    227,
                                    201,
                                    197,
                                    170,
                                    159,
                                    this.perimeter_picture_data
                                ]
                            }
                        ]
                    });
                }
            },
            // 上传dcm文件
            update(e) {
                // 检查患者信息是否完整
                if (!this.patient.patient_id || !this.patient.name || !this.patient.gender || !this.patient.age || !this.patient.phone || !this.patient.body_part) {
                    this.$message.error('请填写完整的患者信息');
                    return;
                }

                this.percentage = 0;
                this.dialogTableVisible = true;
                this.url_1 = "";
                this.url_2 = "";
                this.srcList = [];
                this.srcList1 = [];
                this.wait_return = "";
                this.wait_upload = "";
                this.feature_list = [];
                let myChart_area = this.$echarts.init(document.getElementById("area"));
                myChart_area.setOption({
                    series: [
                        {
                            data: [""]
                        }
                    ]
                });
                this.feat_list = [];
                this.fullscreenLoading = true;
                this.loading = true;
                this.showbutton = false;
                let file = e.target.files[0];
                this.url_1 = this.$options.methods.getObjectURL(file);
                let param = new FormData(); //创建form对象
                param.append("file", file, file.name); //通过append向form对象添加数据
                // 添加患者信息到FormData
                param.append("patient_id", this.patient.patient_id);
                param.append("name", this.patient.name);
                param.append("gender", this.patient.gender);
                param.append("age", this.patient.age);
                param.append("phone", this.patient.phone);
                param.append("body_part", this.patient.body_part);
                // console.log(param.get("file")); //FormData私有类对象，访问不到，可以通过get判断值是否传进去
                //todo aaaa
                var timer = setInterval(() => {
                    this.myFunc();
                }, 30);
                let config = {
                    headers: {"Content-Type": "multipart/form-data"}
                }; //添加请求头
                axios
                    .post(this.server_url+"/upload", param, config)
                    .then(response => {
                        this.percentage = 100;
                        clearInterval(timer);
                        this.url_1 = response.data.image_url;
                        this.srcList.push(this.url_1);
                        this.url_2 = response.data.draw_url;
                        this.srcList1.push(this.url_2);
                        this.fullscreenLoading = false;
                        this.loading = false;

                        this.feat_list = Object.keys(response.data.image_info);

                        for (var i = 0; i < this.feat_list.length; i++) {
                            response.data.image_info[this.feat_list[i]][2] = this.feat_list[i];
                            this.feature_list.push(response.data.image_info[this.feat_list[i]]);
                        }

                        this.feature_list.push(response.data.image_info);
                        this.feature_list_1 = this.feature_list[0];
                        JSON.stringify(response.data.image_info, (key, value) => {
                            console.log(key);
                            console.log(value);
                        });
                        this.dialogTableVisible = false;
                        this.percentage = 0;
                        this.notice1();
                        var areaCompare = document.getElementById("areaCompare");
                        areaCompare.style.display = "none";
                        var areaCompare = document.getElementById("perimeterCompare");
                        areaCompare.style.display = "none";
                        let myChart_area = this.$echarts.init(
                            document.getElementById("area")
                        );
                        let myChart_perimeter = this.$echarts.init(
                            document.getElementById("perimeter")
                        );
                        this.perimeter_picture_data = parseInt(response.data.image_info["perimeter"][1]);
                        this.area_picture_data = parseInt(response.data.image_info["area"][1]);
                        myChart_area.setOption({
                            xAxis: {
                                type: "category",
                                data: ["1", "2", "3", "4", "5", "6", "7", "8"]
                            },
                            yAxis: {
                                type: "value",
                                name: "面积"
                            },
                            areaStyle: {},
                            legend: {
                                data: [""]
                            },
                            series: [
                                {
                                    // 根据名字对应到相应的系列
                                    name: "面积",
                                    type: "line",
                                    data: [
                                        1300,
                                        1290,
                                        1272,
                                        1123.5,
                                        1123,
                                        1092,
                                        1086,
                                        response.data.image_info["area"][1]
                                    ]
                                }
                            ]
                        });

                        myChart_perimeter.setOption({
                            xAxis: {
                                type: "category",
                                data: ["1", "2", "3", "4", "5", "6", "7", "8"]
                            },
                            yAxis: {
                                type: "value",
                                name: "周长"
                            },
                            areaStyle: {},
                            series: [
                                {
                                    // 根据名字对应到相应的系列
                                    name: "周长",
                                    type: "line",
                                    data: [
                                        250,
                                        243,
                                        227,
                                        201,
                                        197,
                                        170,
                                        159,
                                        response.data.image_info["perimeter"]
                                    ]
                                }
                            ]
                        });
                        // 保存诊断结果到数据库
                        this.saveDiagnosisResult(response.data.image_info);
                    });
                },
            // 下载 点击按钮从服务器获取文件
            downTemplate() {
                axios({
                    method: "get",
                    url:
                        "http://localhost:5003/download",
                    responseType: "blob"
                }).then(res => {
                    this.downloads(res.data, res.headers.filename);

                    if (res.status === 200) {
                        this.$message({
                            message: "下载成功",
                            type: "success"
                        });
                        if (this.active == 0) {
                            this.next();
                        }
                    } else {
                        this.$message({
                            showClose: true,
                            message: "下载失败，请重试",
                            type: "error"
                        });
                    }
                });
            },
            myFunc() {
                if (this.percentage + 33 < 99) {
                    this.percentage = this.percentage + 33;
                    console.log(this.percentage);
                } else {
                    this.percentage = 99;
                }
            },
            drawChart() {
                // 基于准备好的dom，初始化echarts实例
                let myChart_area = this.$echarts.init(document.getElementById("area"));
                let myChart_perimeter = this.$echarts.init(
                    document.getElementById("perimeter")
                );
                // 指定图表的配置项和数据
                myChart_area.setOption({
                    title: {
                        text: "肿瘤面积变化",
                        subtext: "Tumor Area Change",
                        left: "center"
                    },
                    legend: {
                        data: [""]
                    },
                    tooltip: {},

                    grid: {
                        //显示数据的图表位于当前canvas的坐标轴
                        x: 40, 
                        y: 55,
                        x2: 80,
                        y2: 140, // 增加y2值，为x轴标签留出更多空间
                        borderWidth: 1
                    },

                    toolbox: {
                        show: true,
                        feature: {
                            dataZoom: {
                                yAxisIndex: "none"
                            },
                            dataView: {readOnly: false},
                            magicType: {type: ["line", "bar"]},
                            restore: {},
                            saveAsImage: {}
                        }
                    },
                    xAxis: {
                        type: "category",
                        boundaryGap: false,
                        data: [],
                        name: "治疗时间",
                        nameLocation: "end", // 将标题放到横坐标右边
                        nameTextStyle: {
                            fontSize: 14
                        },
                        axisLabel: {
                            rotate: 90 // 旋转标签以避免重叠
                        }
                    },
                    yAxis: {
                        type: "value",
                        name: "肿瘤面积",
                        nameTextStyle: {
                            padding: 4,
                            fontSize: 14
                        }
                    },
                    series: [
                        {
                            name: "面积",
                            type: "bar",
                            data: []
                        }
                    ]
                });
                myChart_perimeter.setOption({
                    title: {
                        text: "肿瘤周长变化",
                        subtext: "Tumor Circumference Change",
                        left: "center"
                    },
                    legend: {
                        data: [""]
                    },
                    tooltip: {},

                    grid: {
                        //显示数据的图表位于当前canvas的坐标轴
                        x: 40, 
                        y: 55,
                        x2: 80,
                        y2: 140, // 增加y2值，为x轴标签留出更多空间
                        borderWidth: 1
                    },

                    toolbox: {
                        show: true,
                        feature: {
                            dataZoom: {
                                yAxisIndex: "none"
                            },
                            dataView: {readOnly: false},
                            magicType: {type: ["line", "bar"]},
                            restore: {},
                            saveAsImage: {}
                        }
                    },
                    xAxis: {
                        type: "category",
                        boundaryGap: false,
                        data: [],
                        name: "治疗时间",
                        nameLocation: "end", // 将标题放到横坐标右边
                        nameTextStyle: {
                            fontSize: 14
                        },
                        axisLabel: {
                            rotate: 90 // 旋转标签以避免重叠
                        }
                    },
                    yAxis: {
                        type: "value",
                        name: "肿瘤周长",
                        nameTextStyle: {
                            padding: 4,
                            fontSize: 14
                        }
                    },
                    series: [
                        {
                            name: "周长",
                            type: "bar",
                            data: []
                        }
                    ]
                });
            },
            // 创建模板下载链接
            downloads(data, name) {
                if (!data) {
                    return;
                }
                let url = window.URL.createObjectURL(new Blob([data]));
                let link = document.createElement("a");
                link.style.display = "none";
                link.href = url;
                link.setAttribute("download", `肿瘤CT图文件.zip`);
                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link);
                window.URL.revokeObjectURL(url);
            },
            welcome() {
                axios({
                    method: "get",
                    url:
                        "http://localhost:5003/download",
                    responseType: "blob"
                }).then(res => {
                    this.downloads(res.data, res.headers.filename);
                    if (res.status === 200) {
                        this.$message({
                            message: "下载成功",
                            type: "success"
                        });
                        this.centerDialogVisible = false;
                        this.next();
                    } else {
                        this.$message({
                            showClose: true,
                            message: "下载失败，请重试",
                            type: "error"
                        });
                    }
                });
            },
            notice1() {
                this.$notify({
                    title: "预测成功",
                    message:
                        "点击图片可以查看大图，图片下方会显示肿瘤区域的一些特征值来供医生参考，辅助诊断",
                    duration: 0,
                    type: "success"
                });
            },
            // 从数据库加载患者信息
            loadPatientInfo() {
                if (!this.patient.patient_id) {
                    this.$message.error('请输入患者ID');
                    return;
                }

                axios.get(this.server_url + '/get_patient_info', {
                    params: {
                        patient_id: this.patient.patient_id
                    }
                }).then(response => {
                    if (response.data.status === 1) {
                        this.patient = response.data.patient;
                        this.$message.success('患者信息加载成功');
                    } else {
                        this.$message.warning('未找到该患者信息');
                    }
                }).catch(error => {
                    this.$message.error('加载患者信息失败');
                    console.error(error);
                });
            },
            // 从数据库加载历史诊断数据
            loadHistoryDiagnoses() {
                if (!this.patient.patient_id) {
                    this.$message.error('请输入患者ID');
                    return;
                }

                axios.get(this.server_url + '/get_history_diagnoses', {
                    params: {
                        patient_id: this.patient.patient_id
                    }
                }).then(response => {
                    if (response.data.status === 1) {
                        // 处理历史诊断数据，更新图表
                        this.updateCharts(response.data.diagnoses);
                        this.$message.success('历史诊断数据加载成功');
                    } else {
                        this.$message.warning('未找到该患者的历史诊断数据');
                    }
                }).catch(error => {
                    this.$message.error('加载历史诊断数据失败');
                    console.error(error);
                });
            },
            // 更新图表
            updateCharts(diagnoses) {
                // 处理历史诊断数据，更新面积和周长对比图表
                if (diagnoses.length > 0) {
                    // 按诊断时间排序
                    diagnoses.sort((a, b) => new Date(a.diagnosis_date) - new Date(b.diagnosis_date));

                    // 提取面积和周长数据
                    const areaData = diagnoses.map(d => d.area);
                    const perimeterData = diagnoses.map(d => d.perimeter);

                    // 提取诊断时间并格式化（包含时分秒）
                    const diagnosisDates = diagnoses.map(d => {
                        const date = new Date(d.diagnosis_date);
                        return date.toLocaleString('zh-CN', { 
                            year: 'numeric', 
                            month: '2-digit', 
                            day: '2-digit',
                            hour: '2-digit',
                            minute: '2-digit',
                            second: '2-digit'
                        });
                    });

                    // 更新面积对比图表
                    let myChart_area = this.$echarts.init(document.getElementById('area'));
                    myChart_area.setOption({
                        grid: {
                            // 调整网格位置，增加x轴下方空间和左侧空间
                            x: 40, 
                            y: 55,
                            x2: 80,
                            y2: 140, // 增加y2值，为x轴标签留出更多空间
                            borderWidth: 1
                        },
                        xAxis: {
                            type: "category",
                            data: diagnosisDates,
                            name: "治疗时间",
                            nameLocation: "end", // 将标题放到横坐标右边
                            nameTextStyle: {
                                fontSize: 14
                            },
                            axisLabel: {
                                rotate: 90, // 旋转标签以避免重叠
                                interval: 0 // 显示所有标签
                            }
                        },
                        yAxis: {
                            type: "value",
                            name: "面积",
                            min: function(value) {
                                return Math.floor(value.min * 0.9); // 设置最小值为数据最小值的90%
                            },
                            max: function(value) {
                                return Math.ceil(value.max * 1.1); // 设置最大值为数据最大值的110%
                            }
                        },
                        areaStyle: {},
                        legend: {
                            data: [""]
                        },
                        series: [
                            {
                                name: "面积",
                                type: "line",
                                data: areaData
                            }
                        ]
                    });

                    // 更新周长对比图表
                    let myChart_perimeter = this.$echarts.init(document.getElementById('perimeter'));
                    myChart_perimeter.setOption({
                        grid: {
                            // 调整网格位置，增加x轴下方空间和左侧空间
                            x: 40,
                            y: 55,
                            x2: 80,
                            y2: 140, // 增加y2值，为x轴标签留出更多空间
                            borderWidth: 1
                        },
                        xAxis: {
                            type: "category",
                            data: diagnosisDates,
                            name: "治疗时间",
                            nameLocation: "end", // 将标题放到横坐标右边
                            nameTextStyle: {
                                fontSize: 14
                            },
                            axisLabel: {
                                rotate: 90, // 旋转标签以避免重叠
                                interval: 0 // 显示所有标签
                            }
                        },
                        yAxis: {
                            type: "value",
                            name: "周长",
                            min: function(value) {
                                return Math.floor(value.min * 0.9); // 设置最小值为数据最小值的90%
                            },
                            max: function(value) {
                                return Math.ceil(value.max * 1.1); // 设置最大值为数据最大值的110%
                            }
                        },
                        areaStyle: {},
                        series: [
                            {
                                name: "周长",
                                type: "line",
                                data: perimeterData
                            }
                        ]
                    });
                }
            },
            // 保存诊断结果到数据库
            saveDiagnosisResult(image_info) {
                // 诊断结果已经在后端保存，重新加载历史数据更新图表
                this.$message.success('诊断结果已保存到数据库');
                // 重新加载历史诊断数据以更新图表
                this.loadHistoryDiagnoses();
            },
            // 测试AI模型连通性
            testModelConnection() {
                if (!this.aiSettings.apiUrl || !this.aiSettings.apiKey || !this.aiSettings.modelName) {
                    this.$message.error('请填写完整的AI模型设置');
                    return;
                }

                // 添加用户消息
                this.aiMessages.push({
                    content: '测试模型连通性',
                    type: 'user',
                    timestamp: new Date().toLocaleString()
                });

                // 添加AI响应占位
                const aiMessage = {
                    content: '',
                    displayContent: '',
                    type: 'ai',
                    loading: true,
                    timestamp: new Date().toLocaleString()
                };

                this.aiMessages.push(aiMessage);

                // 调用AI模型API测试连通性
                this.streamTestConnection(aiMessage);
            },

            // 流式测试模型连通性
            async streamTestConnection(message) {
                try {
                    // 构建测试请求
                    const controller = new AbortController();
                    const signal = controller.signal;

                    const response = await fetch(this.aiSettings.apiUrl, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                            'Authorization': `Bearer ${this.aiSettings.apiKey}`
                        },
                        body: JSON.stringify({
                            model: this.aiSettings.modelName,
                            messages: [
                                {
                                    role: 'system',
                                    content: '你是一个测试助手，只需要回复"测试成功"'
                                },
                                {
                                    role: 'user',
                                    content: '测试连接'
                                }
                            ],
                            stream: true
                        }),
                        signal
                    });

                    if (!response.ok) {
                        throw new Error(`HTTP error! Status: ${response.status}`);
                    }

                    const reader = response.body.getReader();
                    const decoder = new TextDecoder();

                    let fullContent = '';

                    while (true) {
                        const { done, value } = await reader.read();

                        if (done) {
                            message.loading = false;
                            if (fullContent.includes('测试成功')) {
                                message.content = '测试成功，模型连通性正常';
                                this.$message.success('模型连通性测试成功');
                            } else {
                                message.content = '测试失败，模型返回异常';
                                this.$message.error('模型连通性测试失败');
                            }
                            break;
                        }

                        // 解码数据
                        const chunk = decoder.decode(value, { stream: true });

                        // 处理SSE格式数据
                        const lines = chunk.split('\n').filter(line => line.trim() !== '');

                        for (const line of lines) {
                            if (line.startsWith('data: ')) {
                                const data = line.substring(6);

                                if (data === '[DONE]') {
                                    message.loading = false;
                                    continue;
                                }

                                try {
                                    const parsed = JSON.parse(data);
                                    const content = parsed.choices[0].delta.content || '';
                                    fullContent += content;

                                    // 更新显示内容
                                    message.content = fullContent;
                                    message.displayContent = fullContent;
                                } catch (error) {
                                    console.error('解析响应失败:', error);
                                }
                            }
                        }
                    }
                } catch (error) {
                    console.error('测试模型连通性失败:', error);
                    message.loading = false;
                    message.content = `测试失败: ${error.message}`;
                    this.$message.error('模型连通性测试失败，请检查网络连接或API设置');
                }
            },
            // AI智能分析
            analyzeWithAI() {
                if (!this.aiSettings.apiUrl || !this.aiSettings.apiKey || !this.aiSettings.modelName) {
                    this.$message.error('请填写完整的AI模型设置');
                    return;
                }

                if (!this.patient.patient_id) {
                    this.$message.error('请输入患者ID');
                    return;
                }

                // 添加用户消息
                this.aiMessages.push({
                    content: '请分析患者的肿瘤变化情况',
                    type: 'user',
                    timestamp: new Date().toLocaleString()
                });

                // 添加AI响应占位
                const aiMessage = {
                    content: '',
                    displayContent: '',
                    type: 'ai',
                    loading: true,
                    timestamp: new Date().toLocaleString()
                };

                this.aiMessages.push(aiMessage);

                // 调用AI模型API获取患者数据并分析
                this.streamAiResponse(aiMessage);
            },

            // 流式接收AI响应
            async streamAiResponse(message) {
                try {
                    // 先获取患者数据
                    const patientData = await this.fetchPatientData();
                    if (!patientData) {
                        message.loading = false;
                        message.content = '获取患者数据失败，请确保患者ID正确';
                        return;
                    }

                    // 构建AI模型请求
                    const controller = new AbortController();
                    const signal = controller.signal;

                    const response = await fetch(this.aiSettings.apiUrl, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                            'Authorization': `Bearer ${this.aiSettings.apiKey}`
                        },
                        body: JSON.stringify({
                            model: this.aiSettings.modelName,
                            messages: [
                                {
                                    role: 'system',
                                    content: '你是一个肿瘤辅助诊断系统的AI助手，负责分析患者的肿瘤变化情况。'
                                },
                                {
                                    role: 'user',
                                    content: `请分析以下患者的肿瘤变化情况：\n\n患者信息：${JSON.stringify(patientData.patient_info, null, 2)}\n\n历史诊断数据：${JSON.stringify(patientData.diagnosis_history, null, 2)}\n\n请提供详细的分析结果，包括肿瘤变化趋势、形态特征变化、治疗效果评估和建议。`
                                }
                            ],
                            stream: true
                        }),
                        signal
                    });

                    if (!response.ok) {
                        throw new Error(`HTTP error! Status: ${response.status}`);
                    }

                    const reader = response.body.getReader();
                    const decoder = new TextDecoder();

                    let fullContent = '';

                    while (true) {
                        const { done, value } = await reader.read();

                        if (done) {
                            message.loading = false;
                            break;
                        }

                        // 解码数据
                        const chunk = decoder.decode(value, { stream: true });

                        // 处理SSE格式数据
                        const lines = chunk.split('\n').filter(line => line.trim() !== '');

                        for (const line of lines) {
                            if (line.startsWith('data: ')) {
                                const data = line.substring(6);

                                if (data === '[DONE]') {
                                    message.loading = false;
                                    continue;
                                }

                                try {
                                    const parsed = JSON.parse(data);
                                    const content = parsed.choices[0].delta.content || '';
                                    fullContent += content;

                                    // 更新显示内容
                                    message.content = fullContent;
                                    message.displayContent = fullContent;
                                } catch (error) {
                                    console.error('解析响应失败:', error);
                                }
                            }
                        }
                    }
                } catch (error) {
                    console.error('调用AI模型失败:', error);
                    message.loading = false;
                    message.content = `调用AI模型失败: ${error.message}`;
                }
            },

            // 获取患者数据
            async fetchPatientData() {
                try {
                    const response = await axios.post('http://127.0.0.1:5003/get_history_data', {
                        patient_id: this.patient.patient_id
                    });

                    if (response.data.status === 1) {
                        return response.data;
                    } else {
                        return null;
                    }
                } catch (error) {
                    console.error('获取患者数据失败:', error);
                    return null;
                }
            },
            // 重置对话
            resetConversation() {
                this.aiMessages = [];
                this.$message.success('对话已重置');
            },

            // 格式化AI返回的结果
            formatAiResponse(content) {
                if (!content) return '';

                // 处理换行符
                content = content.replace(/\n/g, '<br>');

                // 处理分隔线
                content = content.replace(/^---$/gim, '<hr>');

                // 处理标题（支持任意数量的空格）
                content = content.replace(/^###\s+(.*$)/gim, '<h3>$1</h3>');
                content = content.replace(/^##\s+(.*$)/gim, '<h2>$1</h2>');
                content = content.replace(/^#\s+(.*$)/gim, '<h1>$1</h1>');

                // 处理粗体
                content = content.replace(/\*\*(.*?)\*\*/gim, '<strong>$1</strong>');

                // 处理斜体
                content = content.replace(/\*(.*?)\*/gim, '<em>$1</em>');

                // 处理链接
                content = content.replace(/\[([^\]]+)\]\(([^)]+)\)/gim, '<a href="$2" target="_blank">$1</a>');

                // 处理代码行
                content = content.replace(/`([^`]+)`/gim, '<code>$1</code>');

                // 处理无序列表
                const ulRegex = /((?:^- .*?<br>)+)/gim;
                content = content.replace(ulRegex, (match) => {
                    const items = match.replace(/^- (.*?)(?:<br>|$)/gim, '<li>$1</li>');
                    return `<ul>${items}</ul>`;
                });

                // 处理有序列表
                const olRegex = /((?:^\d+\. .*?<br>)+)/gim;
                content = content.replace(olRegex, (match) => {
                    const items = match.replace(/^\d+\. (.*?)(?:<br>|$)/gim, '<li>$1</li>');
                    return `<ol>${items}</ol>`;
                });

                // 处理引用
                content = content.replace(/^> (.*$)/gim, '<blockquote>$1</blockquote>');

                // 处理表格
                // 匹配表格行，包括表头和数据行
                const tableRegex = /((?:^\|.*?<br>)+)/gim;
                content = content.replace(tableRegex, (match) => {
                    const rows = match.split('<br>').filter(row => row.trim() !== '');
                    if (rows.length < 2) return match; // 至少需要表头和分隔行

                    let tableHTML = '<table style="border-collapse: collapse; width: 100%; margin: 10px 0;">';

                    // 处理表头
                    const headerRow = rows[0];
                    const headers = headerRow.split('|').filter(cell => cell.trim() !== '');
                    tableHTML += '<thead><tr>';
                    headers.forEach(header => {
                        tableHTML += `<th style="border: 1px solid #ddd; padding: 8px; text-align: left;">${header.trim()}</th>`;
                    });
                    tableHTML += '</tr></thead>';

                    // 跳过分隔行，处理数据行
                    for (let i = 2; i < rows.length; i++) {
                        const dataRow = rows[i];
                        const cells = dataRow.split('|').filter(cell => cell.trim() !== '');
                        tableHTML += '<tr>';
                        cells.forEach(cell => {
                            tableHTML += `<td style="border: 1px solid #ddd; padding: 8px;">${cell.trim()}</td>`;
                        });
                        tableHTML += '</tr>';
                    }

                    tableHTML += '</table>';
                    return tableHTML;
                });

                return content;
            },
            // 切换AI模型设置展开/收起
            toggleAiSettings() {
                this.showAiSettings = !this.showAiSettings;
            },
            // 保存AI设置到localStorage
            saveAiSettings(settings) {
                try {
                    localStorage.setItem('aiSettings', JSON.stringify(settings));
                } catch (error) {
                    console.error('保存AI设置失败:', error);
                }
            },
            // 从localStorage加载AI设置
            loadAiSettings() {
                try {
                    const savedSettings = localStorage.getItem('aiSettings');
                    if (savedSettings) {
                        this.aiSettings = JSON.parse(savedSettings);
                    }
                } catch (error) {
                    console.error('加载AI设置失败:', error);
                }
            },
            // 手动保存AI设置
            saveAiSettingsManually() {
                try {
                    localStorage.setItem('aiSettings', JSON.stringify(this.aiSettings));
                    this.$message.success('AI设置保存成功');
                    // 保存成功后自动收起设置面板
                    this.showAiSettings = false;
                } catch (error) {
                    console.error('保存AI设置失败:', error);
                    this.$message.error('保存AI设置失败');
                }
            }
        },
        mounted() {
            this.drawChart();
        }
    };
</script>

<style>
.el-button {
    padding: 12px 20px !important;
}

#hello p {
    font-size: 15px !important;
    /*line-height: 25px;*/
}

.n1 .el-step__description {
    padding-right: 20%;
    font-size: 14px;
    line-height: 20px;
    /* font-weight: 400; */
}
</style>

<style scoped>
* {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}

/* AI辅助诊断样式 */
.ai-message {
    margin-bottom: 15px;
    max-width: 80%;
}

.user-message {
    margin-left: auto;
}

.ai-message {
    margin-right: auto;
}

.message-header {
    font-size: 12px;
    color: #999;
    margin-bottom: 5px;
}

.message-content {
    padding: 10px;
    border-radius: 8px;
    background-color: #f5f7fa;
    line-height: 1.5;
}

.user-message .message-content {
    background-color: #409eff;
    color: white;
}

.ai-chat-container {
    border: 1px solid #e4e7ed;
    border-radius: 4px;
    padding: 10px;
}

.loading-indicator {
    display: flex;
    align-items: center;
    margin-top: 5px;
}

.loading-indicator span {
    display: inline-block;
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background-color: #409EFF;
    margin-right: 4px;
    animation: loading 1.4s infinite ease-in-out both;
}

.loading-indicator span:nth-child(1) {
    animation-delay: -0.32s;
}

.loading-indicator span:nth-child(2) {
    animation-delay: -0.16s;
}

@keyframes loading {
    0%, 80%, 100% {
        transform: scale(0);
    }
    40% {
        transform: scale(1);
    }
}

.ai-settings-form {
    margin-top: 10px;
}

.dialog_info {
    margin: 20px auto;
}

.text {
    font-size: 14px;
}

.item {
    margin-bottom: 18px;
}

.clearfix:before,
.clearfix:after {
    display: table;
    content: "";
}

.clearfix:after {
    clear: both;
}

.box-card {
    width: 680px;
    height: 200px;
    border-radius: 8px;
    margin-top: -20px;
}

.divider {
    width: 50%;
}

#CT {
    display: flex;
    height: 100%;
    width: 70%;
    flex-wrap: wrap;
    justify-content: center;
    margin: 0 auto;
    margin-right: 0px;
    max-width: 1200px;
    /* background-color: RGB(239, 249, 251); */
    /* box-shadow: 0 2px 4px rgba(0, 0, 0, 0.12), 0 0 6px rgba(0, 0, 0, 0.04); */
}

#CT_image_1 {
    width: 90%;
    height: 40%;
    /* background-color: RGB(239, 249, 251); */
    margin: 0px auto;
    padding: 0px auto;
    /* box-shadow: 0 2px 4px rgba(0, 0, 0, 0.12), 0 0 6px rgba(0, 0, 0, 0.04); */
    margin-right: 180px;
    margin-bottom: 0px;
    border-radius: 4px;
}

#CT_image {
    margin-bottom: 60px;
    margin-left: 30px;
    margin-top: 5px;
}

.image_1 {
    width: 275px;
    height: 260px;
    background: #ffffff;
    box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.img_info_1 {
    height: 30px;
    width: 275px;
    text-align: center;
    background-color: #21b3b9;
    line-height: 30px;
}

.demo-image__preview1 {
    width: 250px;
    height: 290px;
    margin: 20px 60px;
    float: left;
}

.demo-image__preview2 {
    width: 250px;
    height: 290px;

    margin: 20px 460px;
    /* background-color: green; */
}

.error {
    margin: 100px auto;
    width: 50%;
    padding: 10px;
    text-align: center;
}

.block-sidebar {
    position: fixed;
    display: none;
    left: 50%;
    margin-left: 600px;
    top: 350px;
    width: 60px;
    z-index: 99;
}

.block-sidebar .block-sidebar-item {
    font-size: 50px;
    color: lightblue;
    text-align: center;
    line-height: 50px;
    margin-bottom: 20px;
    cursor: pointer;
    display: block;
}

div {
    display: block;
}

.block-sidebar .block-sidebar-item:hover {
    color: #187aab;
}

.download_bt {
    padding: 10px 16px !important;
}

#upfile {
    width: 104px;
    height: 45px;
    background-color: #187aab;
    color: #fff;
    text-align: center;
    line-height: 45px;
    border-radius: 3px;
    box-shadow: 0 0 2px 0 rgba(0, 0, 0, 0.1), 0 2px 2px 0 rgba(0, 0, 0, 0.2);
    color: #fff;
    font-family: "Source Sans Pro", Verdana, sans-serif;
    font-size: 0.875rem;
}

.file {
    width: 200px;
    height: 130px;
    position: absolute;
    left: -20px;
    top: 0;
    z-index: 1;
    -moz-opacity: 0;
    -ms-opacity: 0;
    -webkit-opacity: 0;
    opacity: 0; /*css属性&mdash;&mdash;opcity不透明度，取值0-1*/
    filter: alpha(opacity=0);
    cursor: pointer;
}

#upload {
    position: relative;
    margin: 0px 0px;
}

#download {
    padding: 0px;
    margin: 0px 0px;
}

.patient {
    margin: 50px auto;
    margin-bottom: 100px;
    /* margin-right: 100px; */
    background-color: #187aab;
    border-radius: 5px;
    box-shadow: 0 0 2px 0 rgba(0, 0, 0, 0.1), 0 2px 2px 0 rgba(0, 0, 0, 0.2);
    color: #fff;
    font-family: "Source Sans Pro", Verdana, sans-serif;
    font-size: 0.875rem;
    line-height: 1;
    padding: 0.75rem 1.5rem;
}

#Content {
    width: 85%;
    height: 1000px;
    background-color: #ffffff;
    margin: 15px auto;
    display: flex;
    min-width: 1200px;
    /* border: 1px solid #e4e7ed; */
    /* box-shadow: 0 2px 4px rgba(0, 0, 0, 0.12), 0 0 6px rgba(0, 0, 0, 0.04); */
}

#aside {
    width: 25%;
    background-color: #ffffff;
    padding: 30px;
    margin-right: 80px;
    /* background-color: RGB(239, 249, 251); */
    /* box-shadow: 0 2px 4px rgba(0, 0, 0, 0.12), 0 0 6px rgba(0, 0, 0, 0.04); */
    height: 800px;
}

.divider {
    background-color: #eaeaea !important;
    height: 2px !important;
    width: 100%;
    margin-bottom: 50px;
}

.divider_1 {
    background-color: #ffffff;
    height: 2px !important;
    width: 100%;
    margin-bottom: 20px;
    margin: 20px auto;
}

.steps {
    font-family: "lucida grande", "lucida sans unicode", lucida, helvetica,
    "Hiragino Sans GB", "Microsoft YaHei", "WenQuanYi Micro Hei", sans-serif;
    color: #21b3b9;
    text-align: center;
    margin: 15px auto;
    font-size: 20px;
    font-weight: bold;
    text-align: center;
}

.step_1 {
    /*color: #303133 !important;*/
    margin: 20px 26px;
}

#info_patient {
    margin-top: 10px;
    margin-right: 160px;
}
</style>

