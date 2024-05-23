import { Button, Radio, Upload } from "antd";
import React, { useEffect, useMemo, useRef, useState } from "react";
import ImgCrop from "antd-img-crop";
import type { GetProp, UploadFile, UploadProps } from "antd";
// import { useStyles } from "./style";
import style from "./index.module.less";
import pic2 from "../assets/scut.jpg";
import { CaretLeftOutlined, CaretRightOutlined } from "@ant-design/icons";
export const Header = () => {
  return (
    <h2
      style={{
        height: "100px",
        backgroundColor: "rgb(58,97,196)",
        textAlign: "center",
        lineHeight: "100px",
        borderRadius: "4px",
        margin: 0,
      }}
    >
      胎儿脑部磁共振数据处理平台
    </h2>
  );
};

export const Center = () => {
  const [data, setData] = useState<any>(null);
  const [state_01, setState_01] = useState<boolean>(false);
  const [state_02, setState_02] = useState<boolean>(false);
  const [state_03, setState_03] = useState<boolean>(false);
  return (
    <div
      style={{
        display: "flex",
        margin: "4px 0",
      }}
    >
      <Sider
        setData={setData}
        state_03={state_03}
        setState_03={setState_03}
        state_01={state_01}
        setState_01={setState_01}
        state_02={state_02}
        setState_02={setState_02}
      />
      <Content
        data={data}
        state_03={state_03}
        setState_03={setState_03}
        state_01={state_01}
        setState_01={setState_01}
        state_02={state_02}
        setState_02={setState_02}
      />
    </div>
  );
};

const Sider = ({
  setData,
  state_01,
  setState_01,
  state_02,
  setState_02,
  state_03,
  setState_03,
}: {
  setData: any;
  state_01: boolean;
  setState_01: any;
  state_02: boolean;
  setState_02: any;
  state_03: boolean;
  setState_03: any;
}) => {
  // const { styles } = useStyles();

  useEffect(() => {
    let myForm = document.getElementById("submitButton");
    const handleSubmit = async () => {
      // const div_01 = document.getElementById("image_01");
      // div_01.innerHTML = "";
      // const div_02 = document.getElementById("image_02");
      // div_02.innerHTML = "";
      // const div_03 = document.getElementById("image_03");
      // div_03.innerHTML = "";
      const fileInput = document.getElementById("fileInput");
      const file = fileInput?.files[0];
      const formData = new FormData();
      formData.append("file", file);
      await fetch("http://127.0.0.1:5000/split_Prototype", {
        method: "POST",
        body: formData,
      })
        .then((response: any) => {
          console.log("shinibaba", response);
          setData(response);
          setState_03(!state_03);
        })
        .catch((error: any) => {
          console.log(error);
        });
      setState_01(!state_01);
      setState_02(!state_02);
    };
    myForm?.addEventListener("click", handleSubmit);

    return () => {
      myForm?.removeEventListener("click", handleSubmit);
    };
  }, []);

  useEffect(() => {
    let myForm = document.getElementById("submitButton1");
    const handleSubmit1 = () => {
      const fileInput = document.getElementById("fileInput1");
      const file = fileInput?.files[0];
      const formData = new FormData();
      formData.append("file", file);
      fetch("http://127.0.0.1:5000/post_example", {
        method: "POST",
        body: formData,
      })
        .then((response: any) => {
          console.log(response);
          // setData(response);
        })
        .catch((error: any) => {
          console.log(error);
        });
    };
    myForm?.addEventListener("click", handleSubmit1);

    return () => {
      myForm?.removeEventListener("click", handleSubmit1);
    };
  }, []);

  return (
    <div
      style={{
        height: "630px",
        marginRight: "4px",
        flex: "1",
        display: "flex",
        justifyContent: "space-around",
        alignItems: "center",
        flexDirection: "column",
        backgroundColor: "#778899",
        borderRadius: "4px",
      }}
    >
      <div
        style={{
          display: "flex",
          flexDirection: "column",
          justifyContent: "center",
          alignItems: "center",
        }}
      >
        <Radio.Group defaultValue={0}>
          <Radio value={0}>DynUNet算法</Radio>
        </Radio.Group>
        <div
          style={{
            textAlign: "center",
          }}
        >
          注：单文件和文件夹根据输入文件类型只选其一,每次上传前需清空输出
        </div>
        <div
          style={{
            marginTop: "15px",
            width: "80%",
            display: "flex",
            justifyContent: "space-around",
          }}
        >
          <Button
            onClick={() => {
              fetch("http://127.0.0.1:5000/call_Model", {
                method: "GET",
              }).then((res) => {
                console.log(res);
              });
            }}
          >
            调用算法
          </Button>
          <Button
            onClick={async () => {
              // const div_01 = document.getElementById("image_01");
              // div_01.innerHTML = "";
              // const div_02 = document.getElementById("image_02");
              // div_02.innerHTML = "";
              const div_03 = document.getElementById("image_03");
              div_03.innerHTML = "";
              const ima_Array = document.querySelectorAll("img");
              ima_Array.forEach((e) => {
                e.src = "";
              });
              // ima_Array.forEach((e, index) => {
              //   console.log(index, e.src);
              // });
              await fetch("http://127.0.0.1:5000/clear_output", {
                method: "GET",
              })
                .then((res) => {
                  console.log(res);
                })
                .finally(() => {
                  setState_03(!state_03);
                });
              // setState_01(!state_01);
              // setState_02(!state_02);
            }}
          >
            清空输出
          </Button>
        </div>
      </div>
      <form
        // action="http://127.0.0.1:5000/post"
        // method="post"
        encType="multipart/form-data"
        id="my_form"
      >
        <input type="file" id="fileInput" name="file" />
        <input type="button" id="submitButton" value="单文件上传" />
      </form>
      <form encType="multipart/form-data" id="my_form1">
        <input type="file" id="fileInput1" name="file1" />
        <input type="button" id="submitButton1" value="多文件上传" />
      </form>
      <Button
        onClick={() => {
          fetch("http://127.0.0.1:5000/open_folder", {
            method: "GET",
          }).then((res) => {
            console.log(res);
          });
        }}
      >
        打开图片文件夹
      </Button>
    </div>
  );
};

const Content = ({
  data,
  state_01,
  setState_01,
  state_02,
  setState_02,
  state_03,
  setState_03,
}: {
  data: any;
  state_01: boolean;
  setState_01: any;
  state_02: boolean;
  setState_02: any;
  state_03: boolean;
  setState_03: any;
}) => {
  const [c1, setC1] = useState<number>(0);
  const [c2, setC2] = useState<number>(0);
  const [c3, setC3] = useState<number>(0);

  const [images_03, setImages_03] = useState<any>({});

  const div_03 = useMemo(() => {
    return document.getElementById("image_03");
  }, []);
  const div_02 = useMemo(() => {
    return document.getElementById("image_02");
  }, []);
  const div_01 = useMemo(() => {
    return document.getElementById("image_01");
  }, []);
  const doms_01 = useRef<any>(null);
  const doms_02 = useRef<any>(null);
  const doms_03 = useRef<any>(null);

  useEffect(() => {
    const images_03 = import.meta.glob(
      "../../sourceData/bpv-fetal-infer/output_result/output_result_03/*.(png|jpg|jpeg|gif|svg)"
    );
    // console.log("shinibaba", Object.keys(images_03).length);
    setImages_03(images_03);
    // console.log("image_03_margin", doms_03.current.indicators);
  }, [state_03]);
  // console.log("laoaab", images_03, Object.keys(images_03).length);
  useEffect(() => {
    if (data && div_03) {
      div_03.innerHTML = "";
    }
    if (div_03) {
      // 遍历 images 对象
      let i = 0;
      if (Object.keys(images_03).length !== 0) {
        const images = images_03;
        // console.log("laoaaa", images);
        for (const path in images) {
          // 通过路径获取加载函数
          // const loadImage = images[path];
          // 创建图片元素
          const img = document.createElement("img");
          // console.log("laoaac", images[path]);
          // 设置图片的属性
          img.src = path; // 设置图片的源路径
          img.width = 300; // 设置图片的宽度
          img.height = 300; // 设置图片的高度
          img.id = `imag3_${i}`;
          img.style.marginLeft = "25px";
          img.style.marginRight = "25px";
          img.className = "image_03_margin";
          ++i;
          // 将图片元素添加到页面中的某个元素中
          div_03.appendChild(img); // 添加到 body 元素中
          // // 加载图片并获取其 URL
          // loadImage().then((module) => {
          //   const imageUrl = module.default;
          //   // 在这里可以使用 imageUrl，例如将其赋值给 img 标签的 src 属性
          //   console.log(`Image URL for ${path}:`, imageUrl);
          // });
        }
      }
      doms_03.current = {
        div_03,
        count: i,
        indicators: null,
      };
      doms_03.current.indicators =
        document.querySelectorAll(".image_03_margin");
      init(div_03);
    }
  }, [images_03]);
  const images_01 = useMemo(() => {
    return import.meta.glob(
      "../../sourceData/bpv-fetal-infer/output_result/output_result_01/*.(png|jpg|jpeg|gif|svg)"
    );
  }, [state_01]);
  useEffect(() => {
    if (data && div_01) {
      div_01.innerHTML = "";
    }
    if (div_01) {
      // 遍历 images 对象
      let i = 0;
      if (Object.keys(images_01).length !== 0) {
        const images = images_01;
        for (const path in images) {
          // 通过路径获取加载函数
          // const loadImage = images[path];
          // 创建图片元素
          const img = document.createElement("img");

          // 设置图片的属性
          img.src = path; // 设置图片的源路径
          img.width = 300; // 设置图片的宽度
          img.height = 300; // 设置图片的高度
          img.id = `imag1_${i}`;
          img.style.marginLeft = "25px";
          img.style.marginRight = "25px";
          img.className = "image_01_margin";
          ++i;
          // 将图片元素添加到页面中的某个元素中
          div_01.appendChild(img); // 添加到 body 元素中
        }
        doms_01.current = {
          div_01,
          count: i,
          indicators: null,
        };
        doms_01.current.indicators =
          document.querySelectorAll(".image_01_margin");
        init(div_01);
      }
    }
  }, [div_01, data, images_01, state_01]);

  const images_02 = useMemo(() => {
    return import.meta.glob(
      "../../sourceData/bpv-fetal-infer/output_result/output_result_02/*.(png|jpg|jpeg|gif|svg)"
    );
  }, [state_02]);
  useEffect(() => {
    if (data && div_02) {
      div_02.innerHTML = "";
    }
    if (div_02) {
      // 遍历 images 对象
      let i = 0;
      if (Object.keys(images_02).length !== 0) {
        const images = images_02;
        for (const path in images) {
          // 通过路径获取加载函数
          // const loadImage = images[path];
          // 创建图片元素
          const img = document.createElement("img");

          // 设置图片的属性
          img.src = path; // 设置图片的源路径
          img.width = 300; // 设置图片的宽度
          img.height = 300; // 设置图片的高度
          img.id = `imag2_${i}`;
          img.style.marginLeft = "25px";
          img.style.marginRight = "25px";
          img.className = "image_02_margin";
          ++i;
          // 将图片元素添加到页面中的某个元素中
          div_02.appendChild(img); // 添加到 body 元素中
          // // 加载图片并获取其 URL
          // loadImage().then((module) => {
          //   const imageUrl = module.default;
          //   // 在这里可以使用 imageUrl，例如将其赋值给 img 标签的 src 属性
          //   console.log(`Image URL for ${path}:`, imageUrl);
          // });
        }
        doms_02.current = {
          div_02,
          count: i,
          indicators: null,
        };
        doms_02.current.indicators =
          document.querySelectorAll(".image_02_margin");
        init(div_02);
      }
    }
  }, [div_02, data, images_02, state_02]);

  function MoveTo(index: number, div_00: any) {
    div_00.style.transform = `translateX(-${index * 350}px)`;
    div_00.style.transition = "transform 0.5s";
  }
  const init = useMemo(() => {
    return (dom: any) => {
      if (dom?.firstElementChild) {
        const firstCloned = dom?.firstElementChild?.cloneNode(true);
        const lastCloned = dom?.lastElementChild?.cloneNode(true);
        dom.appendChild(firstCloned);
        dom.insertBefore(lastCloned, dom.firstElementChild);
        lastCloned.style.marginLeft = "-325px";
        lastCloned.style.marginRight = "25px";
      } else {
        return;
      }
    };
  }, []);

  function moveLeft(count: number, setC: any, len: number, div_00: any) {
    if (count === 0) {
      div_00.style.transition = "none";
      div_00.style.transform = `translateX(-${len * 350}px)`;
      div_00?.clientHeight;
      setC(() => {
        MoveTo(len - 1, div_00);
        return len - 1;
      });
    } else {
      setC(() => {
        MoveTo(count - 1, div_00);
        return count - 1;
      });
    }
  }

  function moveRight(count: number, setC: any, div_00: any, len: number) {
    if (count === len - 1) {
      div_00.style.transition = "none";
      div_00.style.transform = `translateX(${350}px)`;
      div_00?.clientHeight;
      setC(() => {
        MoveTo(0, div_00);
        return 0;
      });
    } else {
      setC(() => {
        MoveTo(count + 1, div_00);
        return count + 1;
      });
    }
  }

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
        borderRadius: "4px",
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
            position: "relative",
            overflow: "hidden",
          }}
        >
          <div
            id="image_01"
            style={{
              width: "350px",
              height: "300px",
              // backgroundColor: "yellow",
              borderRight: "solid 1px white",
              // overflow: "hidden",
              display: "flex",
            }}
          ></div>
          <div
            id="arrowLeft_01"
            style={{
              position: "absolute",
              top: 0,
              left: 0,
              backgroundColor: "#AFEEEE",
              height: 300,
              width: 25,
              display: "flex",
              justifyContent: "center",
              alignItems: "center",
            }}
          >
            <CaretLeftOutlined
              style={{ fontSize: "30px", color: "black" }}
              onClick={() => {
                moveLeft(c1, setC1, doms_01.current.count, div_01);
              }}
            />
          </div>
          <div
            id="arrowRight_01"
            style={{
              position: "absolute",
              right: 0,
              top: 0,
              backgroundColor: "#AFEEEE",
              height: 300,
              width: 25,
              display: "flex",
              justifyContent: "center",
              alignItems: "center",
            }}
          >
            <CaretRightOutlined
              style={{ fontSize: "30px", color: "black" }}
              onClick={() => {
                moveRight(c1, setC1, div_01, doms_01.current.count);
              }}
            />
          </div>
          <div
            style={{
              color: "white",
              position: "absolute",
              right: "35px",
              bottom: "20px",
              fontSize: "14px",
            }}
          >
            {doms_01.current ? c1 + 1 + "/" + doms_01.current.count : ""}
          </div>
        </div>
        <div
          style={{
            width: "350px",
            height: "300px",
            // backgroundImage: `url(${pic2})`,
            backgroundSize: "contain",
          }}
        ></div>
      </div>
      <div
        style={{
          width: "700px",
          height: "300px",
          // backgroundColor: "blue",
          display: "flex",
          border: "solid 1px white",
        }}
      >
        <div
          style={{
            position: "relative",
            overflow: "hidden",
          }}
        >
          <div
            id="image_02"
            style={{
              width: "350px",
              height: "300px",
              // backgroundColor: "yellow",
              borderRight: "solid 1px white",
              // overflow: "hidden",
              display: "flex",
            }}
          ></div>
          <div
            id="arrowLeft_02"
            style={{
              position: "absolute",
              top: 0,
              left: 0,
              backgroundColor: "#AFEEEE",
              height: 300,
              width: 25,
              display: "flex",
              justifyContent: "center",
              alignItems: "center",
            }}
          >
            <CaretLeftOutlined
              style={{ fontSize: "30px", color: "black" }}
              onClick={() => {
                moveLeft(c2, setC2, doms_02.current.count, div_02);
              }}
            />
          </div>
          <div
            id="arrowRight_02"
            style={{
              position: "absolute",
              right: 0,
              top: 0,
              backgroundColor: "#AFEEEE",
              height: 300,
              width: 25,
              display: "flex",
              justifyContent: "center",
              alignItems: "center",
            }}
          >
            <CaretRightOutlined
              style={{ fontSize: "30px", color: "black" }}
              onClick={() => {
                moveRight(c2, setC2, div_02, doms_02.current.count);
              }}
            />
          </div>
          <div
            style={{
              color: "white",
              position: "absolute",
              right: "35px",
              bottom: "20px",
              fontSize: "14px",
            }}
          >
            {doms_02.current ? c2 + 1 + "/" + doms_02.current.count : ""}
          </div>
        </div>
        <div
          style={{
            position: "relative",
            overflow: "hidden",
          }}
        >
          <div
            id="image_03"
            style={{
              width: "350px",
              height: "300px",
              // backgroundColor: "yellow",
              borderRight: "solid 1px white",
              // overflow: "hidden",
              display: "flex",
            }}
          ></div>
          <div
            id="arrowLeft_03"
            style={{
              position: "absolute",
              top: 0,
              left: 0,
              backgroundColor: "#AFEEEE",
              height: 300,
              width: 25,
              display: "flex",
              justifyContent: "center",
              alignItems: "center",
            }}
          >
            <CaretLeftOutlined
              style={{ fontSize: "30px", color: "black" }}
              onClick={() => {
                moveLeft(c3, setC3, doms_03.current.count, div_03);
              }}
            />
          </div>
          <div
            id="arrowRight_03"
            style={{
              position: "absolute",
              right: 0,
              top: 0,
              backgroundColor: "#AFEEEE",
              height: 300,
              width: 25,
              display: "flex",
              justifyContent: "center",
              alignItems: "center",
            }}
          >
            <CaretRightOutlined
              style={{ fontSize: "30px", color: "black" }}
              onClick={() => {
                moveRight(c3, setC3, div_03, doms_03.current.count);
              }}
            />
          </div>
          <div
            style={{
              color: "white",
              position: "absolute",
              right: "35px",
              bottom: "20px",
              fontSize: "14px",
            }}
          >
            {doms_03.current ? c3 + 1 + "/" + doms_03.current.count : ""}
          </div>
        </div>
      </div>
    </div>
  );
};

type FileType = Parameters<GetProp<UploadProps, "beforeUpload">>[0];
