<template>
    <div id="Header">
        <!-- CT图像处理字（可删除放图片） -->
        <div id="word">
            <h1>{{msg}}</h1>
        </div>
    </div>
</template>
<script>
    export default {
        name: "Header",
        data() {
            return {
                msg: "肿瘤辅助诊断系统",
                activeIndex: "1"
            };
        },
        methods: {
            handleSelect(key, keyPath) {
                // eslint-disable-next-line no-console
                console.log(key, keyPath);
            }
        }
    };
</script>
<style scoped>
    #Header {
        padding: 30px 0 0 0;
        width: 90%;
        margin: 10px auto;
    }

    #word {
        margin: 0 auto;
        height: 60px;
        /* box-shadow: 0 2px 4px rgba(0, 0, 0, 0.12), 0 0 6px rgba(0, 0, 0, 0.04); */
        line-height: 60px;
        text-align: center;
    }

    h1 {
        color: #21b3b9;
        letter-spacing: 20px;
        font-size: 2.3em;
        margin: 0;
        text-indent: 20px;
    }


    .top-left-edition span i {
        float: left;
        margin-right: 10px;
    }

    i,
    input,
    label {
        vertical-align: middle;
    }

    i {
        border: 0;
        display: block;
        cursor: pointer;
    }

    .top-left-edition span {
        float: left;
        font-size: 16px;
        color: #999999;
        line-height: 24px;
        margin-right: 40px;
    }
</style>


