export interface ISphinxPreview {
  SphinxPreview: (
    srcdir: string,
    confdir: string,
    outdir: string
  ) => { build: () => { status: string; warnings: string } };
}
