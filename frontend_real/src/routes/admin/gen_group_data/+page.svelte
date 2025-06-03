<script>
    import axios from 'axios';

    // 表单数据
    let formData = {
        student_id: '',
        teacher_name1: '',
        teacher_name2: '',
        teacher_name3: ''
    };

    // 状态变量
    let isLoading = false;
    let notification = '';
    let notificationType = '';

    // 提交表单创建评分组
    async function createGroup() {
        try {
            // 表单验证
            if (!formData.student_id || !formData.teacher_name1 || 
                !formData.teacher_name2 || !formData.teacher_name3) {
                notification = '请填写所有必填字段';
                notificationType = 'alert-warning';
                return;
            }

            isLoading = true;
            notification = '正在创建评分组数据，请稍候...';
            notificationType = 'alert-info';

            // 调用后端 API 创建评分组
            const response = await axios.post('http://127.0.0.1:8000/api/v1/data-gen/gen_group_data', null, {
                params: {
                    student_id: formData.student_id,
                    teacher_name1: formData.teacher_name1,
                    teacher_name2: formData.teacher_name2,
                    teacher_name3: formData.teacher_name3
                }
            });

            notification = response.data.message || '评分组创建成功';
            notificationType = 'alert-success';
            
            // 重置表单
            formData = {
                student_id: '',
                teacher_name1: '',
                teacher_name2: '',
                teacher_name3: ''
            };
            
        } catch (err) {
            console.error('创建评分组失败:', err);
            notification = `操作失败: ${err.response?.data?.detail || err.message}`;
            notificationType = 'alert-error';
        } finally {
            isLoading = false;
        }
    }
</script>

<div class="container mx-auto p-4">
    <h1 class="text-2xl font-bold mb-6">评分组数据生成</h1>

    <!-- 通知区域 -->
    {#if notification}
        <div class="alert {notificationType} mb-6">
            <span>{notification}</span>
        </div>
    {/if}

    <!-- 表单区域 -->
    <div class="card bg-base-100 shadow-xl mb-6">
        <div class="card-body">
            <h2 class="card-title mb-4">创建评分组</h2>
            <p>正式考虑通过excel导入数据</p>
            
            <div class="form-control mb-4">
                <label class="label">
                    <span class="label-text">学生学号</span>
                </label>
                <input 
                    type="text" 
                    class="input input-bordered w-full" 
                    placeholder="学生学号"
                    bind:value={formData.student_id}
                />
            </div>

            <div class="form-control mb-4">
                <label class="label">
                    <span class="label-text">指导教师</span>
                </label>
                <input 
                    type="text" 
                    class="input input-bordered w-full" 
                    placeholder="指导教师姓名"
                    bind:value={formData.teacher_name1}
                />
            </div>

            <div class="form-control mb-4">
                <label class="label">
                    <span class="label-text">评阅教师</span>
                </label>
                <input 
                    type="text" 
                    class="input input-bordered w-full" 
                    placeholder="评阅教师姓名"
                    bind:value={formData.teacher_name2}
                />
            </div>

            <div class="form-control mb-6">
                <label class="label">
                    <span class="label-text">答辩委员会</span>
                </label>
                <input 
                    type="text" 
                    class="input input-bordered w-full" 
                    placeholder="答辩委员会教师姓名"
                    bind:value={formData.teacher_name3}
                />
            </div>

            <div class="card-actions justify-end">
                <button 
                    class="btn btn-primary" 
                    on:click={createGroup} 
                    disabled={isLoading}
                >
                    {#if isLoading}
                        <span class="loading loading-spinner"></span>
                        处理中...
                    {:else}
                        创建评分组
                    {/if}
                </button>
            </div>
        </div>
    </div>
</div>