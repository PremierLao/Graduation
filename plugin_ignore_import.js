export default function ignoreImportErrorsPlugin() {
  return {
    name: "ignore-import-errors",
    resolveId(source) {
      // 检查导入的文件路径是否以指定的路径开头
      if (
        source.startsWith("../../sourceData/bpv-fetal-infer/output_result/")
      ) {
        // 在任何环境下都返回 false，以阻止 Vite 报告相关的导入错误
        return false;
      }
    },
  };
}
