import Foundation
import PDFKit

// Keep PDF page boundaries so notes can cite local PDF pages.
for path in CommandLine.arguments.dropFirst() {
    let url = URL(fileURLWithPath: path)
    guard let doc = PDFDocument(url: url), doc.pageCount > 0 else {
        fputs("INVALID PDF: \(path)\n", stderr)
        continue
    }
    var result = "Source: \(url.lastPathComponent)\nPages: \(doc.pageCount)\n"
    for index in 0..<doc.pageCount {
        result += "\n===== PDF PAGE \(index + 1) =====\n"
        let page = doc.page(at: index)!
        let original = page.string ?? ""
        if original.trimmingCharacters(in: .whitespacesAndNewlines).count < 80 {
            result += "[Sparse text layer: inspect the original PDF]\n"
        }
        result += original.isEmpty ? "[No extractable text]" : original
        result += "\n"
    }
    let dest = URL(fileURLWithPath: "paper-text").appendingPathComponent(url.deletingPathExtension().lastPathComponent + ".txt")
    do {
        try result.write(to: dest, atomically: true, encoding: .utf8)
        print("\(url.lastPathComponent): \(doc.pageCount) pages")
    } catch {
        fputs("WRITE ERROR: \(error)\n", stderr)
    }
}
