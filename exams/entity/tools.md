<tools>
<tool name="read_file">
  <description>Read the contents of a file.</description>
  <parameters>
    <param name="path" type="string" required="true">File path relative to project root.</param>
  </parameters>
</tool>
<tool name="write_file">
  <description>Create or overwrite a file.</description>
  <parameters>
    <param name="path" type="string" required="true">File path relative to project root.</param>
    <param name="content" type="string" required="true">Full file content.</param>
  </parameters>
</tool>
<tool name="list_directory">
  <description>List entries in a directory.</description>
  <parameters>
    <param name="path" type="string" required="true">Directory path relative to project root.</param>
  </parameters>
</tool>
<tool name="move_file">
  <description>Move or rename a file.</description>
  <parameters>
    <param name="src" type="string" required="true">Source path.</param>
    <param name="dst" type="string" required="true">Destination path.</param>
  </parameters>
</tool>
<tool name="search_files">
  <description>Search file contents for a pattern. Returns matching lines with file paths.</description>
  <parameters>
    <param name="pattern" type="string" required="true">Search pattern (regex).</param>
    <param name="path" type="string" required="false">Directory to search in. Defaults to project root.</param>
  </parameters>
</tool>
<tool name="bash">
  <description>Execute a shell command and return its stdout/stderr.</description>
  <parameters>
    <param name="command" type="string" required="true">The command to run.</param>
  </parameters>
</tool>
</tools>

You have exclusive filesystem access — no other user or process modifies files during this session. Do not re-read files already seen in this conversation.

When responding, emit your reasoning alongside tool calls. Use parallel tool calls when actions are independent.
