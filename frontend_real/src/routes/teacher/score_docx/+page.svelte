<script>
    import { onMount } from "svelte";
    import axios from "axios";
    
    // 教师用户名
    let username = "";
    let loading = true;
    let students = []; // 存储教师管理的学生信息
    let selectedStudent = null; // 当前选中的学生
    
    // 表单数据 - 更新为匹配BaseScoreDocx模型
    let formData = {
        student_name: "",
        content1: "", 
        score1: null,  // 改为数字类型
        content2: "",
        score2: null,  // 改为数字类型
        content3: "",
        score3: null   // 改为数字类型
    };
    
    // 教师角色
    let teacherRole = ""; // "teacher1", "teacher2", "teacher3"
    
    // 消息通知
    let notification = "";
    let notificationType = "";
    let currentStudentId = null;
    let existingRecord = false; // 标记是否存在已有评分记录
    
    onMount(() => {
        if (typeof window !== "undefined") {
            username = localStorage.getItem("username") || "用户";
            fetchStudents();
        }
    });
    
    // 获取教师管理的学生信息
    async function fetchStudents() {
        try {
            loading = true;
            const response = await axios.get(`http://127.0.0.1:8000/api/v1/group/${username}`);
            
            if (response.data && response.data.length > 0) {
                students = response.data;
            } else {
                notification = "未找到您管理的学生信息";
                notificationType = "alert-warning";
            }
        } catch (error) {
            console.error("获取学生信息失败:", error);
            notification = "获取学生信息失败，请稍后重试";
            notificationType = "alert-error";
        } finally {
            loading = false;
        }
    }
    
    // 获取学生已有的评分记录
    async function fetchStudentScoreRecord(studentId) {
        try {
            const response = await axios.get(`http://127.0.0.1:8000/api/v1/group/student/${studentId}`);
            if (response.data) {
                // 已有评分记录
                existingRecord = true;
                return response.data;
            }
        } catch (error) {
            if (error.response && error.response.status === 404) {
                // 没有评分记录，这是正常情况
                existingRecord = false;
                return null;
            }
            console.error("获取学生评分记录失败:", error);
            notification = "获取评分记录失败，请稍后重试";
            notificationType = "alert-error";
            return null;
        }
    }
    
    // 选择学生
    async function selectStudent(student) {
        selectedStudent = student;
        currentStudentId = student.student_id;
        
        // 判断当前教师角色
        if (student.teacher_name1 === username) {
            teacherRole = "teacher1"; // 指导教师
        } else if (student.teacher_name2 === username) {
            teacherRole = "teacher2"; // 评阅教师
        } else if (student.teacher_name3 === username) {
            teacherRole = "teacher3"; // 答辩委员会
        } else {
            teacherRole = ""; // 未知角色
        }
        
        // 获取学生已有评分记录
        const scoreRecord = await fetchStudentScoreRecord(currentStudentId);
        
        // 准备默认评语模板
        const defaultTemplates = {
            content1: "该学生在毕业设计过程中表现优异，能积极参与讨论，认真完成任务...",
            content2: "该学生设计思路清晰，实现完整，文档规范，代码结构合理...",
            content3: "该学生答辩表现良好，回答问题准确，对项目理解深入，能清晰阐述..."
        };
        
        // 根据已有记录或默认模板设置表单数据
        formData = {
            student_name: student.student_name || "",
            content1: scoreRecord?.content1 || (teacherRole === "teacher1" ? defaultTemplates.content1 : ""),
            score1: scoreRecord?.score1 || (teacherRole === "teacher1" ? 80 : null),
            content2: scoreRecord?.content2 || (teacherRole === "teacher2" ? defaultTemplates.content2 : ""),
            score2: scoreRecord?.score2 || (teacherRole === "teacher2" ? 80 : null),
            content3: scoreRecord?.content3 || (teacherRole === "teacher3" ? defaultTemplates.content3 : ""),
            score3: scoreRecord?.score3 || (teacherRole === "teacher3" ? 80 : null)
        };
        
        notification = "";
    }
    
    // 提交评分
    async function handleSubmit() {
        if (!selectedStudent || !currentStudentId) {
            notification = "请先选择一名学生";
            notificationType = "alert-warning";
            return;
        }
        
        // 验证是否有权限
        if (teacherRole === "") {
            notification = "您没有对该学生的评分权限";
            notificationType = "alert-error";
            return;
        }
        
        try {
            // 根据教师角色验证对应字段
            if (teacherRole === "teacher1" && (!formData.content1 || formData.score1 === null)) {
                notification = "请填写指导教师评语和分数";
                notificationType = "alert-warning";
                return;
            }
            if (teacherRole === "teacher2" && (!formData.content2 || formData.score2 === null)) {
                notification = "请填写评阅教师评语和分数";
                notificationType = "alert-warning";
                return;
            }
            if (teacherRole === "teacher3" && (!formData.content3 || formData.score3 === null)) {
                notification = "请填写答辩委员会评语和分数";
                notificationType = "alert-warning";
                return;
            }
            
            // 验证分数是否合法
            let scoreField = null;
            if (teacherRole === "teacher1") scoreField = formData.score1;
            if (teacherRole === "teacher2") scoreField = formData.score2;
            if (teacherRole === "teacher3") scoreField = formData.score3;
            
            if (scoreField === null || scoreField < 0 || scoreField > 100) {
                notification = "分数必须是0-100之间的整数";
                notificationType = "alert-error";
                return;
            }
            
            let response;
            if (existingRecord) {
                // 已有记录，更新
                response = await axios.put(
                    `http://127.0.0.1:8000/api/v1/group/student/${currentStudentId}`,
                    formData
                );
            } else {
                // 无记录，创建
                response = await axios.post(
                    `http://127.0.0.1:8000/api/v1/group/student/${currentStudentId}`,
                    formData
                );
            }
            
            if (response.data) {
                existingRecord = true; // 提交后肯定存在记录
                notification = "评分提交成功";
                notificationType = "alert-success";
            }
        } catch (error) {
            console.error("提交评分失败:", error);
            notification = "评分提交失败，请稍后重试";
            notificationType = "alert-error";
        }
    }
    
    // 计算平均分
    $: averageScore = formData.score1 && formData.score2 && formData.score3 
        ? Math.round((formData.score1 + formData.score2 + formData.score3) / 3) 
        : null;
</script>

<div class="bg-gray-50 max-h-screen text-gray-800 p-4">
    <h2 class="text-xl font-semibold mb-4">毕业设计成绩评分</h2>
    
    {#if notification}
        <div class={`alert ${notificationType} shadow-lg mt-2 mb-4`}>
            <div>
                {#if notificationType === 'alert-success'}
                    <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
                {:else if notificationType === 'alert-error'}
                    <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
                {:else}
                    <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" /></svg>
                {/if}
                <span>{notification}</span>
            </div>
        </div>
    {/if}
    
    {#if loading}
        <div class="flex justify-center my-8">
            <span class="loading loading-spinner loading-lg"></span>
        </div>
    {:else}
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-4">
            <!-- 左侧：学生列表 -->
            <div class="bg-white rounded-lg shadow p-4">
                <h3 class="text-lg font-medium mb-3">您参与评审的学生</h3>
                
                {#if students.length === 0}
                    <div class="text-gray-500 text-center py-4">
                        未找到您参与评审的学生
                    </div>
                {:else}
                    <div class="max-h-[600px] overflow-y-auto">
                        {#each students as student}
                            <div 
                                class="p-3 border-b cursor-pointer hover:bg-gray-50 {selectedStudent && selectedStudent.student_id === student.student_id ? 'bg-blue-50' : ''}"
                                on:click={() => selectStudent(student)}
                            >
                                <div class="font-medium">{student.student_name || `学生${student.student_id}`}</div>
                                <div class="text-sm text-gray-600 truncate">
                                    {#if student.teacher_name1 === username}
                                        <span class="badge badge-primary">指导教师</span>
                                    {:else if student.teacher_name2 === username}
                                        <span class="badge badge-secondary">评阅教师</span>
                                    {:else if student.teacher_name3 === username}
                                        <span class="badge badge-accent">答辩委员</span>
                                    {/if}
                                </div>
                            </div>
                        {/each}
                    </div>
                {/if}
            </div>
            
            <!-- 右侧：评分表单 -->
            <div class="lg:col-span-2">
                {#if selectedStudent}
                    <div class="bg-white rounded-lg shadow p-4">
                        <h3 class="text-lg font-medium mb-3">
                            成绩评审表填写
                            {#if teacherRole === "teacher1"}
                                <span class="badge badge-primary ml-2">指导教师</span>
                            {:else if teacherRole === "teacher2"}
                                <span class="badge badge-secondary ml-2">评阅教师</span>
                            {:else if teacherRole === "teacher3"}
                                <span class="badge badge-accent ml-2">答辩委员</span>
                            {/if}
                        </h3>
                        
                        <div class="bg-slate-100 p-3 rounded-md mb-4">
                            <p class="font-medium mb-2">基本信息</p>
                            <div class="grid grid-cols-1 md:grid-cols-2 gap-2">
                                <div>
                                    <span class="text-gray-600">学生：</span>
                                    <span class="font-medium">{selectedStudent.student_name || `学生${selectedStudent.student_id}`}</span>
                                </div>
                                <div>
                                    <span class="text-gray-600">学号：</span>
                                    <span class="font-medium">{selectedStudent.student_id}</span>
                                </div>
                            </div>
                        </div>
                        
                        <!-- 已有评分情况概览 -->
                        {#if existingRecord}
                            <div class="p-3 bg-gray-50 rounded-md mb-4">
                                <p class="font-medium mb-2">评分情况概览</p>
                                <div class="flex flex-wrap gap-4">
                                    <div>
                                        <span class="text-gray-600">指导教师：</span>
                                        <span class="font-medium">{formData.score1 !== null ? `${formData.score1}分` : '未评分'}</span>
                                    </div>
                                    <div>
                                        <span class="text-gray-600">评阅教师：</span>
                                        <span class="font-medium">{formData.score2 !== null ? `${formData.score2}分` : '未评分'}</span>
                                    </div>
                                    <div>
                                        <span class="text-gray-600">答辩委员会：</span>
                                        <span class="font-medium">{formData.score3 !== null ? `${formData.score3}分` : '未评分'}</span>
                                    </div>
                                    {#if formData.score1 !== null && formData.score2 !== null && formData.score3 !== null}
                                        <div>
                                            <span class="text-gray-600">综合得分：</span>
                                            <span class="font-medium text-primary">{averageScore}分</span>
                                        </div>
                                    {/if}
                                </div>
                            </div>
                        {/if}
                        
                        <form on:submit|preventDefault={handleSubmit} class="space-y-4">
                            <!-- 指导教师评语 -->
                            {#if teacherRole === "teacher1"}
                                <div class="mb-4">
                                    <label class="block bg-slate-100 p-2 rounded-t-md font-medium">指导教师评语：</label>
                                    <textarea 
                                        class="textarea textarea-bordered w-full h-24 rounded-t-none" 
                                        bind:value={formData.content1}
                                        placeholder="请输入评价内容"
                                        required
                                    ></textarea>
                                    <div class="flex items-center mt-2">
                                        <span class="mr-2">分数:</span>
                                        <input 
                                            type="number" 
                                            class="input input-bordered w-20" 
                                            bind:value={formData.score1}
                                            min="0" 
                                            max="100" 
                                            required
                                        />
                                        <span class="ml-2">(0-100分)</span>
                                    </div>
                                </div>
                            {:else if teacherRole === "teacher2"}
                                <!-- 评阅教师评语 -->
                                <div class="mb-4">
                                    <label class="block bg-slate-100 p-2 rounded-t-md font-medium">评阅教师评语：</label>
                                    <textarea 
                                        class="textarea textarea-bordered w-full h-24 rounded-t-none" 
                                        bind:value={formData.content2}
                                        placeholder="请输入评价内容"
                                        required
                                    ></textarea>
                                    <div class="flex items-center mt-2">
                                        <span class="mr-2">分数:</span>
                                        <input 
                                            type="number" 
                                            class="input input-bordered w-20" 
                                            bind:value={formData.score2}
                                            min="0" 
                                            max="100" 
                                            required
                                        />
                                        <span class="ml-2">(0-100分)</span>
                                    </div>
                                </div>
                            {:else if teacherRole === "teacher3"}
                                <!-- 答辩委员会评语 -->
                                <div class="mb-4">
                                    <label class="block bg-slate-100 p-2 rounded-t-md font-medium">答辩委员会（或答辩小组）评语：</label>
                                    <textarea 
                                        class="textarea textarea-bordered w-full h-24 rounded-t-none" 
                                        bind:value={formData.content3}
                                        placeholder="请输入评价内容"
                                        required
                                    ></textarea>
                                    <div class="flex items-center mt-2">
                                        <span class="mr-2">分数:</span>
                                        <input 
                                            type="number" 
                                            class="input input-bordered w-20" 
                                            bind:value={formData.score3}
                                            min="0" 
                                            max="100" 
                                            required
                                        />
                                        <span class="ml-2">(0-100分)</span>
                                    </div>
                                </div>
                            {:else}
                                <div class="alert alert-warning">
                                    <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" /></svg>
                                    <span>您没有对该学生的评分权限</span>
                                </div>
                            {/if}
                            
                            <div class="flex justify-end pt-4">
                                <button 
                                    type="submit" 
                                    class="btn btn-primary"
                                    disabled={!teacherRole}
                                >
                                    {existingRecord ? '更新评分' : '提交评分'}
                                </button>
                            </div>
                        </form>
                    </div>
                {:else}
                    <div class="bg-white rounded-lg shadow p-8 text-center">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-12 w-12 mx-auto text-gray-400 mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 19a2 2 0 01-2-2V7a2 2 0 012-2h4l2 2h4a2 2 0 012 2v1M5 19h14a2 2 0 002-2v-5a2 2 0 00-2-2H9a2 2 0 00-2 2v5a2 2 0 01-2 2z" />
                        </svg>
                        <p class="text-lg text-gray-600">请从左侧选择一名学生进行评分</p>
                    </div>
                {/if}
            </div>
        </div>
    {/if}
</div>