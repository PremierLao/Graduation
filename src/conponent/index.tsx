import { Button, Radio, Upload } from "antd";
import React, { useState } from "react";
import ImgCrop from "antd-img-crop";
import type { GetProp, UploadFile, UploadProps } from "antd";
// import { useStyles } from "./style";
import style from "./index.module.less";
import pic2 from "../assets/pic2.png";
import { UploadOutlined } from "@ant-design/icons";

export const Header = () => {
  return (
    <div
      style={{
        height: "100px",
        backgroundColor: "#778899",
        textAlign: "center",
        lineHeight: "100px",
      }}
    >
      胎儿脑部磁共振数据处理平台
    </div>
  );
};

export const Center = () => {
  return (
    <div
      style={{
        display: "flex",
        margin: "4px 0",
      }}
    >
      <Sider />
      <Content />
    </div>
  );
};

const Sider = () => {
  const props: UploadProps = {
    action: "//jsonplaceholder.typicode.com/posts/",
    listType: "picture",
    previewFile(file) {
      console.log("Your upload file:", file);
      // Your process logic. Here we just mock to the same file
      return fetch("https://next.json-generator.com/api/json/get/4ytyBoLK8", {
        method: "POST",
        body: file,
      })
        .then((res) => res.json())
        .then(({ thumbnail }) => thumbnail);
    },
  };

  const fetchData = async () => {
    const data = await fetch("http://127.0.0.1:5000/post", {
      method: "POSt",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        a: "111",
      }),
    }).then((res) => {
      return res.text();
    });
    console.log(data);
  };

  return (
    <div
      style={{
        height: "630px",
        backgroundColor: "#778899",
        marginRight: "4px",
        flex: "1",
        display: "flex",
        justifyContent: "space-around",
        alignItems: "center",
        flexDirection: "column",
      }}
    >
      <div>
        <Radio.Group>
          <Radio value={0}>算法a</Radio>
        </Radio.Group>
        <Button onClick={fetchData}>分析</Button>
      </div>
      <div>
        <Upload {...props}>
          <Button icon={<UploadOutlined />}>Upload</Button>
        </Upload>
      </div>
    </div>
  );
};

const Content = () => {
  return (
    <div
      style={{
        height: "630px",
        backgroundColor: "#778899",
        flex: "3",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        flexDirection: "column",
      }}
    >
      <div
        style={{
          width: "700px",
          height: "300px",
          display: "flex",
          border: "solid 1px white",
        }}
      >
        <div
          style={{
            width: "350px",
            height: "300px",
            backgroundColor: "red",
            borderRight: "solid 1px white",
          }}
        ></div>
        <div
          style={{
            width: "350px",
            height: "300px",
            backgroundImage: `url(${pic2})`,
            backgroundSize: "contain",
          }}
        ></div>
      </div>
      <div
        style={{
          width: "700px",
          height: "300px",
          backgroundColor: "blue",
          display: "flex",
          border: "solid 1px white",
        }}
      >
        <div
          style={{
            width: "350px",
            height: "300px",
            backgroundColor: "yellow",
            borderRight: "solid 1px white",
          }}
        ></div>
        <div
          style={{
            width: "350px",
            height: "300px",
            backgroundColor: "green",
          }}
        ></div>
      </div>
    </div>
  );
};
