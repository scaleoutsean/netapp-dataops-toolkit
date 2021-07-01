#!/usr/bin/env python3
"""NetApp DataOps Toolkit for Kubernetes Script Interface."""
from netapp_dataops import k8s
from netapp_dataops.k8s import (
    clone_volume,
    create_volume_snapshot,
    InvalidConfigError,
    APIConnectionError,
    create_volume,
    clone_jupyter_lab,
    create_jupyter_lab,
    create_jupyter_lab_snapshot,
    delete_volume_snapshot,
    delete_volume,
    delete_jupyter_lab,
    list_jupyter_labs,
    list_volume_snapshots,
    list_jupyter_lab_snapshots,
    list_volumes,
    restore_jupyter_lab_snapshot,
    restore_volume_snapshot
)


# Define contents of help text
helpTextStandard = '''
The NetApp DataOps Toolkit for Kubernetes is a Python library that makes it simple for data scientists and data engineers to perform various data management tasks, such as provisioning a new data volume, near-instantaneously cloning a data volume, and near-instantaneously snapshotting a data volume for traceability/baselining.

Basic Commands:

\thelp\t\t\t\tPrint help text.
\tversion\t\t\t\tPrint version details.

JupyterLab Management Commands:
Note: To view details regarding options/arguments for a specific command, run the command with the '-h' or '--help' option.

\tclone jupyterlab\t\tCreate a new JupyterLab workspace that is an exact copy of an existing workspace.
\tcreate jupyterlab\t\tProvision a JupyterLab workspace.
\tdelete jupyterlab\t\tDelete an existing JupyterLab workspace.
\tlist jupyterlabs\t\tList all JupyterLab workspaces.
\tcreate jupyterlab-snapshot\tCreate a new snapshot for a JupyterLab workspace.
\tlist jupyterlab-snapshots\tList all snapshots.
\trestore jupyterlab-snapshot\tRestore a snapshot.

Kubernetes Persistent Volume Management Commands (for advanced Kubernetes users):
Note: To view details regarding options/arguments for a specific command, run the command with the '-h' or '--help' option.

\tclone volume\t\t\tCreate a new persistent volume that is an exact copy of an existing persistent volume.
\tcreate volume\t\t\tProvision a new persistent volume.
\tdelete volume\t\t\tDelete an existing persistent volume.
\tlist volumes\t\t\tList all persistent volumes.
\tcreate volume-snapshot\t\tCreate a new snapshot for a persistent volume.
\tdelete volume-snapshot\t\tDelete an existing snapshot.
\tlist volume-snapshots\t\tList all snapshots.
\trestore volume-snapshot\t\tRestore a snapshot.
'''
helpTextCloneJupyterLab = '''
Command: clone jupyterlab

Create a new JupyterLab workspace that is an exact copy of an existing workspace.

Note: Either -s/--source-snapshot-name or -j/--source-workspace-name must be specified. However, only one of these flags (not both) should be specified for a given operation. If -j/--source-workspace-name is specified, then the clone will be created from the current state of the workspace. If -s/--source-snapshot-name is specified, then the clone will be created from a specific snapshot related the source workspace.

Required Options/Arguments:
\t-w, --new-workspace-name=\tName of new workspace (name to be applied to new JupyterLab workspace).

Optional Options/Arguments:
\t-c, --volume-snapshot-class=\tKubernetes VolumeSnapshotClass to use when creating clone. If not specified, "csi-snapclass" will be used. Note: VolumeSnapshotClass must be configured to use Trident.
\t-g, --nvidia-gpu=\t\tNumber of NVIDIA GPUs to allocate to new JupyterLab workspace. Format: '1', '4', etc. If not specified, no GPUs will be allocated.
\t-h, --help\t\t\tPrint help text.
\t-j, --source-workspace-name=\tName of JupyterLab workspace to use as source for clone. Either -s/--source-snapshot-name or -j/--source-workspace-name must be specified.
\t-m, --memory=\t\t\tAmount of memory to reserve for new JupyterLab workspace. Format: '1024Mi', '100Gi', '10Ti', etc. If not specified, no memory will be reserved.
\t-n, --namespace=\t\tKubernetes namespace that source workspace is located in. If not specified, namespace "default" will be used.
\t-p, --cpu=\t\t\tNumber of CPUs to reserve for new JupyterLab workspace. Format: '0.5', '1', etc. If not specified, no CPUs will be reserved.
\t-s, --source-snapshot-name=\tName of Kubernetes VolumeSnapshot to use as source for clone. Either -s/--source-snapshot-name or -j/--source-workspace-name must be specified.

Examples:
\tnetapp_dataops_k8s_cli.py clone jupyterlab --new-workspace-name=project1-experiment1 --source-workspace-name=project1 --nvidia-gpu=1
\tnetapp_dataops_k8s_cli.py clone jupyterlab -w project2-mike -s project2-snap1 -n team1 -g 1 -p 0.5 -m 1Gi
'''
helpTextCloneVolume = '''
Command: clone volume

Create a new persistent volume that is an exact copy of an existing persistent volume.

Note: Either -s/--source-snapshot-name or -v/--source-pvc-name must be specified. However, only one of these flags (not both) should be specified for a given operation. If -v/--source-pvc-name is specified, then the clone will be created from the current state of the volume. If -s/--source-snapshot-name is specified, then the clone will be created from a specific snapshot related the source volume.

Required Options/Arguments:
\t-p, --new-pvc-name=\t\tName of new volume (name to be applied to new Kubernetes PersistentVolumeClaim/PVC).

Optional Options/Arguments:
\t-c, --volume-snapshot-class=\tKubernetes VolumeSnapshotClass to use when creating clone. If not specified, "csi-snapclass" will be used. Note: VolumeSnapshotClass must be configured to use Trident.
\t-h, --help\t\t\tPrint help text.
\t-n, --namespace=\t\tKubernetes namespace that source PersistentVolumeClaim (PVC) is located in. If not specified, namespace "default" will be used.
\t-s, --source-snapshot-name=\tName of Kubernetes VolumeSnapshot to use as source for clone. Either -s/--source-snapshot-name or -v/--source-pvc-name must be specified.
\t-v, --source-pvc-name=\t\tName of Kubernetes PersistentVolumeClaim (PVC) to use as source for clone. Either -s/--source-snapshot-name or -v/--source-pvc-name must be specified.

Examples:
\tnetapp_dataops_k8s_cli.py clone volume --new-pvc-name=project1-experiment1 --source-pvc-name=project1
\tnetapp_dataops_k8s_cli.py clone volume -p project2-mike -s snap1 -n team1
'''
helpTextCreateJupyterLab = '''
Command: create jupyterlab

Provision a JupyterLab workspace.

Required Options/Arguments:
\t-w, --workspace-name=\tName of new JupyterLab workspace.
\t-s, --size=\t\tSize new workspace (i.e. size of backing persistent volume to be created). Format: '1024Mi', '100Gi', '10Ti', etc.

Optional Options/Arguments:
\t-c, --storage-class=\tKubernetes StorageClass to use when provisioning backing volume for new workspace. If not specified, the default StorageClass will be used. Note: The StorageClass must be configured to use Trident or the BeeGFS CSI driver.
\t-g, --nvidia-gpu=\tNumber of NVIDIA GPUs to allocate to JupyterLab workspace. Format: '1', '4', etc. If not specified, no GPUs will be allocated.
\t-h, --help\t\tPrint help text.
\t-i, --image=\t\tContainer image to use when creating workspace. If not specified, "jupyter/tensorflow-notebook" will be used.
\t-m, --memory=\t\tAmount of memory to reserve for JupyterLab workspace. Format: '1024Mi', '100Gi', '10Ti', etc. If not specified, no memory will be reserved.
\t-n, --namespace=\tKubernetes namespace to create new workspace in. If not specified, workspace will be created in namespace "default".
\t-p, --cpu=\t\tNumber of CPUs to reserve for JupyterLab workspace. Format: '0.5', '1', etc. If not specified, no CPUs will be reserved.

Examples:
\tnetapp_dataops_k8s_cli.py create jupyterlab --workspace-name=mike --size=10Gi --nvidia-gpu=2
\tnetapp_dataops_k8s_cli.py create jupyterlab -n dst-test -w dave -i jupyter/scipy-notebook:latest -s 2Ti -c ontap-flexgroup -g 1 -p 0.5 -m 1Gi
'''
helpTextCreateJupyterLabSnapshot = '''
Command: create jupyterlab-snapshot

Create a new snapshot for a JupyterLab workspace.

Required Options/Arguments:
\t-w, --workspace-name=\t\tName of JupyterLab workspace.

Optional Options/Arguments:
\t-c, --volume-snapshot-class=\tKubernetes VolumeSnapshotClass to use when creating snapshot of backing volume for workspace. If not specified, "csi-snapclass" will be used. Note: VolumeSnapshotClass must be configured to use Trident.
\t-h, --help\t\t\tPrint help text.
\t-n, --namespace=\t\tKubernetes namespace that workspace is located in. If not specified, namespace "default" will be used.
\t-s, --snapshot-name=\t\tName of new Kubernetes VolumeSnapshot for workspace. If not specified, will be set to 'ntap-dsutil.<timestamp>'.

Examples:
\tnetapp_dataops_k8s_cli.py create jupyterlab-snapshot --workspace-name=mike
\tnetapp_dataops_k8s_cli.py create jupyterlab-snapshot -w sathish -s snap1 -c ontap -n team1
'''
helpTextCreateVolumeSnapshot = '''
Command: create volume-snapshot

Create a new snapshot for a persistent volume.

Required Options/Arguments:
\t-p, --pvc-name=\t\t\tName of Kubernetes PersistentVolumeClaim (PVC) to create snapshot for.

Optional Options/Arguments:
\t-c, --volume-snapshot-class=\tKubernetes VolumeSnapshotClass to use when creating snapshot. If not specified, "csi-snapclass" will be used. Note: VolumeSnapshotClass must be configured to use Trident.
\t-h, --help\t\t\tPrint help text.
\t-n, --namespace=\t\tKubernetes namespace that PersistentVolumeClaim (PVC) is located in. If not specified, namespace "default" will be used.
\t-s, --snapshot-name=\t\tName of new Kubernetes VolumeSnapshot. If not specified, will be set to 'ntap-dsutil.<timestamp>'.

Examples:
\tnetapp_dataops_k8s_cli.py create volume-snapshot --pvc-name=project1
\tnetapp_dataops_k8s_cli.py create volume-snapshot -p project2 -s snap1 -c ontap -n team1
'''
helpTextCreateVolume = '''
Command: create volume

Provision a new persistent volume.

Required Options/Arguments:
\t-p, --pvc-name=\t\tName of new volume (name to be applied to new Kubernetes PersistentVolumeClaim/PVC).
\t-s, --size=\t\tSize of new volume. Format: '1024Mi', '100Gi', '10Ti', etc.

Optional Options/Arguments:
\t-c, --storage-class=\tKubernetes StorageClass to use when provisioning new volume. If not specified, default StorageClass will be used. Note: The StorageClass must be configured to use Trident or the BeeGFS CSI driver.
\t-h, --help\t\tPrint help text.
\t-n, --namespace=\tKubernetes namespace to create new PersistentVolumeClaim (PVC) in. If not specified, PVC will be created in namespace "default".

Examples:
\tnetapp_dataops_k8s_cli.py create volume --pvc-name=project1 --size=10Gi
\tnetapp_dataops_k8s_cli.py create volume -p datasets -s 10Ti -n team1
\tnetapp_dataops_k8s_cli.py create volume --pvc-name=project2 --size=2Ti --namespace=team2 --storage-class=ontap-flexgroup
'''
helpTextDeleteJupyterLab = '''
Command: delete jupyterlab

Delete an existing JupyterLab workspace.

Required Options/Arguments:
\t-w, --workspace-name=\t\tName of JupyterLab workspace to be deleted.

Optional Options/Arguments:
\t-f, --force\t\t\tDo not prompt user to confirm operation.
\t-h, --help\t\t\tPrint help text.
\t-n, --namespace=\t\tKubernetes namespace that the workspace is located in. If not specified, namespace "default" will be used.
\t-s, --preserve-snapshots\tDo not delete VolumeSnapshots associated with workspace.

Examples:
\tnetapp_dataops_k8s_cli.py delete jupyterlab --workspace-name=mike
\tnetapp_dataops_k8s_cli.py delete jupyterlab -w dave -n dst-test
'''
helpTextDeleteJupyterLabSnapshot = '''
Command: delete jupyterlab-snapshot

Delete an existing JupyterLab workspace snapshot.

Required Options/Arguments:
\t-s, --snapshot-name=\tName of Kubernetes VolumeSnapshot to be deleted.

Optional Options/Arguments:
\t-f, --force\t\tDo not prompt user to confirm operation.
\t-h, --help\t\tPrint help text.
\t-n, --namespace=\tKubernetes namespace that VolumeSnapshot is located in. If not specified, namespace "default" will be used.

Examples:
\tnetapp_dataops_k8s_cli.py delete jupyterlab-snapshot --snapshot-name=snap1
\tnetapp_dataops_k8s_cli.py delete jupyterlab-snapshot -s ntap-dsutil.20210304151544 -n team1
'''
helpTextDeleteVolumeSnapshot = '''
Command: delete volume-snapshot

Delete an existing snapshot.

Required Options/Arguments:
\t-s, --snapshot-name=\tName of Kubernetes VolumeSnapshot to be deleted.

Optional Options/Arguments:
\t-f, --force\t\tDo not prompt user to confirm operation.
\t-h, --help\t\tPrint help text.
\t-n, --namespace=\tKubernetes namespace that VolumeSnapshot is located in. If not specified, namespace "default" will be used.

Examples:
\tnetapp_dataops_k8s_cli.py delete volume-snapshot --snapshot-name=snap1
\tnetapp_dataops_k8s_cli.py delete volume-snapshot -s ntap-dsutil.20210304151544 -n team1
'''
helpTextDeleteVolume = '''
Command: delete volume

Delete an existing persistent volume.

Required Options/Arguments:
\t-p, --pvc-name=\t\t\tName of Kubernetes PersistentVolumeClaim (PVC) to be deleted.

Optional Options/Arguments:
\t-f, --force\t\t\tDo not prompt user to confirm operation.
\t-h, --help\t\t\tPrint help text.
\t-n, --namespace=\t\tKubernetes namespace that PersistentVolumeClaim (PVC) is located in. If not specified, namespace "default" will be used.
\t-s, --preserve-snapshots\tDo not delete VolumeSnapshots associated with PersistentVolumeClaim (PVC).

Examples:
\tnetapp_dataops_k8s_cli.py delete volume --pvc-name=project1
\tnetapp_dataops_k8s_cli.py delete volume -p project2 -n team1
'''
helpTextListJupyterLabs = '''
Command: list jupyterlabs

List all JupyterLab workspaces in a specific namespace.

No options/arguments are required.

Optional Options/Arguments:
\t-h, --help\t\tPrint help text.
\t-n, --namespace=\tKubernetes namespace for which to retrieve list of workspaces. If not specified, namespace "default" will be used.

Examples:
\tnetapp_dataops_k8s_cli.py list jupyterlabs -n team1
\tnetapp_dataops_k8s_cli.py list jupyterlabs --namespace=team2
'''
helpTextListJupyterLabSnapshots = '''
Command: list jupyterlab-snapshots

List all JupyterLab workspace snapshots in a specific namespace.

No options/arguments are required.

Optional Options/Arguments:
\t-h, --help\t\tPrint help text.
\t-n, --namespace=\tKubernetes namespace that Kubernetes VolumeSnapshot is located in. If not specified, namespace "default" will be used.
\t-w, --workspace-name=\tName of JupyterLab workspace to list snapshots for. If not specified, all VolumeSnapshots in namespace will be listed.

Examples:
\tnetapp_dataops_k8s_cli.py list jupyterlab-snapshots --workspace-name=mike
\tnetapp_dataops_k8s_cli.py list jupyterlab-snapshots -n team2
'''
helpTextListVolumeSnapshots = '''
Command: list volume-snapshots

List all persistent volume snapshots in a specific namespace.

No options/arguments are required.

Optional Options/Arguments:
\t-h, --help\t\tPrint help text.
\t-n, --namespace=\tKubernetes namespace that Kubernetes VolumeSnapshot is located in. If not specified, namespace "default" will be used.
\t-p, --pvc-name=\t\tName of Kubernetes PersistentVolumeClaim (PVC) to list snapshots for. If not specified, all VolumeSnapshots in namespace will be listed.

Examples:
\tnetapp_dataops_k8s_cli.py list volume-snapshots --pvc-name=project1
\tnetapp_dataops_k8s_cli.py list volume-snapshots -n team2
'''
helpTextListVolumes = '''
Command: list volumes

List all persistent volumes in a specific namespace.

No options/arguments are required.

Optional Options/Arguments:
\t-h, --help\t\tPrint help text.
\t-n, --namespace=\tKubernetes namespace for which to retrieve list of volumes. If not specified, namespace "default" will be used.

Examples:
\tnetapp_dataops_k8s_cli.py list volumes -n team1
\tnetapp_dataops_k8s_cli.py list volumes --namespace=team2
'''
helpTextRestoreJupyterLabSnapshot = '''
Command: restore jupyterlab-snapshot

Restore a snapshot for a JupyterLab workspace.

Required Options/Arguments:
\t-s, --snapshot-name=\tName of Kubernetes VolumeSnapshot to be restored.

Optional Options/Arguments:
\t-h, --help\t\tPrint help text.
\t-n, --namespace=\tKubernetes namespace that VolumeSnapshot is located in. If not specified, namespace "default" will be used.

Examples:
\tnetapp_dataops_k8s_cli.py restore jupyterlab-snapshot --snapshot-name=mike-snap1
\tnetapp_dataops_k8s_cli.py restore jupyterlab-snapshot -s ntap-dsutil.20210304151544 -n team1
'''
helpTextRestoreVolumeSnapshot = '''
Command: restore volume-snapshot

Restore a snapshot for a persistent volume.

Warning: In order to restore a snapshot, the PersistentVolumeClaim (PVC) associated the snapshot must NOT be mounted to any pods.
Tip: If the PVC associated with the snapshot is currently mounted to a pod that is managed by a deployment, you can scale the deployment to 0 pods using the command `kubectl scale --replicas=0 deployment/<deployment_name>`. After scaling the deployment to 0 pods, you will be able to restore the snapshot. After restoring the snapshot, you can use the `kubectl scale` command to scale the deployment back to the desired number of pods.

Required Options/Arguments:
\t-s, --snapshot-name=\tName of Kubernetes VolumeSnapshot to be restored.

Optional Options/Arguments:
\t-f, --force\t\tDo not prompt user to confirm operation.
\t-h, --help\t\tPrint help text.
\t-n, --namespace=\tKubernetes namespace that VolumeSnapshot is located in. If not specified, namespace "default" will be used.

Examples:
\tnetapp_dataops_k8s_cli.py restore volume-snapshot --snapshot-name=snap1
\tnetapp_dataops_k8s_cli.py restore volume-snapshot -s ntap-dsutil.20210304151544 -n team1
'''


## Function for handling situation in which user enters invalid command
def handleInvalidCommand(helpText: str = helpTextStandard, invalidOptArg: bool = False):
    if invalidOptArg:
        print("Error: Invalid option/argument.")
    else:
        print("Error: Invalid command.")
    print(helpText)
    sys.exit(1)


## Function for getting desired target from command line args
def getTarget(args: list) -> str:
    try:
        target = args[2]
    except:
        handleInvalidCommand()
    return target


## Main function
if __name__ == '__main__':
    import sys, getopt

    # Get desired action from command line args
    try:
        action = sys.argv[1]
    except:
        handleInvalidCommand()

    # Invoke desired action
    if action == "clone":
        # Get desired target from command line args
        target = getTarget(sys.argv)

        # Invoke desired action based on target
        if target in ("volume", "vol", "pvc", "persistentvolumeclaim"):
            newPvcName = None
            sourcePvcName = None
            sourceSnapshotName = None
            volumeSnapshotClass = "csi-snapclass"
            namespace = "default"

            # Get command line options
            try:
                opts, args = getopt.getopt(sys.argv[3:], "hp:c:n:s:v:",
                                           ["help", "new-pvc-name=", "volume-snapshot-class=", "namespace=",
                                            "source-snapshot-name=", "source-pvc-name="])
            except:
                handleInvalidCommand(helpText=helpTextCloneVolume, invalidOptArg=True)

            # Parse command line options
            for opt, arg in opts:
                if opt in ("-h", "--help"):
                    print(helpTextCloneVolume)
                    sys.exit(0)
                elif opt in ("-p", "--new-pvc-name"):
                    newPvcName = arg
                elif opt in ("-c", "--volume-snapshot-class"):
                    volumeSnapshotClass = arg
                elif opt in ("-n", "--namespace"):
                    namespace = arg
                elif opt in ("-s", "--source-snapshot-name"):
                    sourceSnapshotName = arg
                elif opt in ("-v", "--source-pvc-name"):
                    sourcePvcName = arg

            # Check for required options
            if not newPvcName or (not sourceSnapshotName and not sourcePvcName):
                handleInvalidCommand(helpText=helpTextCloneVolume, invalidOptArg=True)
            if sourceSnapshotName and sourcePvcName:
                print(
                    "Error: Both -s/--source-snapshot-name and -v/--source-pvc-name cannot be specified for the same operation.")
                handleInvalidCommand(helpText=helpTextCloneVolume, invalidOptArg=True)

            # Clone volume
            try:
                clone_volume(new_pvc_name=newPvcName, source_pvc_name=sourcePvcName, source_snapshot_name=sourceSnapshotName,
                             volume_snapshot_class=volumeSnapshotClass, namespace=namespace, print_output=True)
            except (InvalidConfigError, APIConnectionError):
                sys.exit(1)

        elif target in ("jupyterlab", "jupyter"):
            newWorkspaceName = None
            sourceWorkspaceName = None
            sourceSnapshotName = None
            volumeSnapshotClass = "csi-snapclass"
            namespace = "default"
            requestNvidiaGpu = None
            requestMemory = None
            requestCpu = None

            # Get command line options
            try:
                opts, args = getopt.getopt(sys.argv[3:], "hw:c:n:s:j:g:m:p:",
                                           ["help", "new-workspace-name=", "volume-snapshot-class=", "namespace=",
                                            "source-snapshot-name=", "source-workspace-name=", "nvidia-gpu=", "memory=",
                                            "cpu="])
            except:
                handleInvalidCommand(helpText=helpTextCloneJupyterLab, invalidOptArg=True)

            # Parse command line options
            for opt, arg in opts:
                if opt in ("-h", "--help"):
                    print(helpTextCloneJupyterLab)
                    sys.exit(0)
                elif opt in ("-w", "--new-workspace-name"):
                    newWorkspaceName = arg
                elif opt in ("-c", "--volume-snapshot-class"):
                    volumeSnapshotClass = arg
                elif opt in ("-n", "--namespace"):
                    namespace = arg
                elif opt in ("-s", "--source-snapshot-name"):
                    sourceSnapshotName = arg
                elif opt in ("-j", "--source-workspace-name"):
                    sourceWorkspaceName = arg
                elif opt in ("-g", "--nvidia-gpu"):
                    requestNvidiaGpu = arg
                elif opt in ("-m", "--memory"):
                    requestMemory = arg
                elif opt in ("-p", "--cpu"):
                    requestCpu = arg

            # Check for required options
            if not newWorkspaceName or (not sourceSnapshotName and not sourceWorkspaceName):
                handleInvalidCommand(helpText=helpTextCloneJupyterLab, invalidOptArg=True)
            if sourceSnapshotName and sourceWorkspaceName:
                print(
                    "Error: Both -s/--source-snapshot-name and -j/--source-workspace-name cannot be specified for the same operation.")
                handleInvalidCommand(helpText=helpTextCloneJupyterLab, invalidOptArg=True)

            # Clone volume
            try:
                clone_jupyter_lab(new_workspace_name=newWorkspaceName, source_workspace_name=sourceWorkspaceName,
                                  source_snapshot_name=sourceSnapshotName, volume_snapshot_class=volumeSnapshotClass,
                                  namespace=namespace, request_cpu=requestCpu, request_memory=requestMemory,
                                  request_nvidia_gpu=requestNvidiaGpu, print_output=True)
            except (InvalidConfigError, APIConnectionError):
                sys.exit(1)

        else:
            handleInvalidCommand()

    elif action == "create":
        # Get desired target from command line args
        target = getTarget(sys.argv)

        # Invoke desired action based on target
        if target in ("volume-snapshot", "volumesnapshot"):
            pvcName = None
            snapshotName = None
            volumeSnapshotClass = "csi-snapclass"
            namespace = "default"

            # Get command line options
            try:
                opts, args = getopt.getopt(sys.argv[3:], "hp:c:n:s:",
                                           ["help", "pvc-name=", "volume-snapshot-class=", "namespace=",
                                            "snapshot-name="])
            except:
                handleInvalidCommand(helpText=helpTextCreateVolumeSnapshot, invalidOptArg=True)

            # Parse command line options
            for opt, arg in opts:
                if opt in ("-h", "--help"):
                    print(helpTextCreateVolumeSnapshot)
                    sys.exit(0)
                elif opt in ("-p", "--pvc-name"):
                    pvcName = arg
                elif opt in ("-c", "--volume-snapshot-class"):
                    volumeSnapshotClass = arg
                elif opt in ("-n", "--namespace"):
                    namespace = arg
                elif opt in ("-s", "--snapshot-name"):
                    snapshotName = arg

            # Check for required options
            if not pvcName:
                handleInvalidCommand(helpText=helpTextCreateVolumeSnapshot, invalidOptArg=True)

            # Create snapshot
            try:
                create_volume_snapshot(pvc_name=pvcName, snapshot_name=snapshotName,
                                       volume_snapshot_class=volumeSnapshotClass, namespace=namespace, print_output=True)
            except (InvalidConfigError, APIConnectionError):
                sys.exit(1)

        elif target in ("volume", "vol", "pvc", "persistentvolumeclaim"):
            pvcName = None
            volumeSize = None
            namespace = "default"
            storageClass = None

            # Get command line options
            try:
                opts, args = getopt.getopt(sys.argv[3:], "hp:s:n:c:",
                                           ["help", "pvc-name=", "size=", "namespace=", "storage-class="])
            except:
                handleInvalidCommand(helpText=helpTextCreateVolume, invalidOptArg=True)

            # Parse command line options
            for opt, arg in opts:
                if opt in ("-h", "--help"):
                    print(helpTextCreateVolume)
                    sys.exit(0)
                elif opt in ("-p", "--pvc-name"):
                    pvcName = arg
                elif opt in ("-s", "--size"):
                    volumeSize = arg
                elif opt in ("-n", "--namespace"):
                    namespace = arg
                elif opt in ("-c", "--storage-class"):
                    storageClass = arg

            # Check for required options
            if not pvcName or not volumeSize:
                handleInvalidCommand(helpText=helpTextCreateVolume, invalidOptArg=True)

            # Create volume
            try:
                create_volume(pvc_name=pvcName, volume_size=volumeSize, storage_class=storageClass, namespace=namespace,
                              print_output=True)
            except (InvalidConfigError, APIConnectionError):
                sys.exit(1)

        elif target in ("jupyterlab", "jupyter"):
            workspaceName = None
            workspaceSize = None
            namespace = "default"
            storageClass = None
            workspaceImage = "jupyter/scipy-notebook:latest"
            requestNvidiaGpu = None
            requestMemory = None
            requestCpu = None

            # Get command line options
            try:
                opts, args = getopt.getopt(sys.argv[3:], "hw:s:n:c:i:g:m:p:",
                                           ["help", "workspace-name=", "size=", "namespace=", "storage-class=",
                                            "image=", "nvidia-gpu=", "memory=", "cpu="])
            except:
                handleInvalidCommand(helpText=helpTextCreateJupyterLab, invalidOptArg=True)

            # Parse command line options
            for opt, arg in opts:
                if opt in ("-h", "--help"):
                    print(helpTextCreateJupyterLab)
                    sys.exit(0)
                elif opt in ("-w", "--workspace-name"):
                    workspaceName = arg
                elif opt in ("-s", "--size"):
                    workspaceSize = arg
                elif opt in ("-n", "--namespace"):
                    namespace = arg
                elif opt in ("-c", "--storage-class"):
                    storageClass = arg
                elif opt in ("-i", "--image"):
                    workspaceImage = arg
                elif opt in ("-g", "--nvidia-gpu"):
                    requestNvidiaGpu = arg
                elif opt in ("-m", "--memory"):
                    requestMemory = arg
                elif opt in ("-p", "--cpu"):
                    requestCpu = arg

            # Check for required options
            if not workspaceName or not workspaceSize:
                handleInvalidCommand(helpText=helpTextCreateJupyterLab, invalidOptArg=True)

            # Create JupyterLab workspace
            try:
                create_jupyter_lab(workspace_name=workspaceName, workspace_size=workspaceSize, storage_class=storageClass,
                                   namespace=namespace, workspace_image=workspaceImage, request_cpu=requestCpu,
                                   request_memory=requestMemory, request_nvidia_gpu=requestNvidiaGpu, print_output=True)
            except (InvalidConfigError, APIConnectionError):
                sys.exit(1)

        elif target in ("jupyterlab-snapshot", "jupyterlabsnapshot", "jupyter-snapshot", "jupytersnapshot"):
            workspaceName = None
            snapshotName = None
            volumeSnapshotClass = "csi-snapclass"
            namespace = "default"

            # Get command line options
            try:
                opts, args = getopt.getopt(sys.argv[3:], "hw:c:n:s:",
                                           ["help", "workspace-name=", "volume-snapshot-class=", "namespace=",
                                            "snapshot-name="])
            except:
                handleInvalidCommand(helpText=helpTextCreateJupyterLabSnapshot, invalidOptArg=True)

            # Parse command line options
            for opt, arg in opts:
                if opt in ("-h", "--help"):
                    print(helpTextCreateJupyterLabSnapshot)
                    sys.exit(0)
                elif opt in ("-w", "--workspace-name"):
                    workspaceName = arg
                elif opt in ("-c", "--volume-snapshot-class"):
                    volumeSnapshotClass = arg
                elif opt in ("-n", "--namespace"):
                    namespace = arg
                elif opt in ("-s", "--snapshot-name"):
                    snapshotName = arg

            # Check for required options
            if not workspaceName:
                handleInvalidCommand(helpText=helpTextCreateJupyterLabSnapshot, invalidOptArg=True)

            # Create snapshot
            try:
                create_jupyter_lab_snapshot(workspace_name=workspaceName, snapshot_name=snapshotName,
                                            volume_snapshot_class=volumeSnapshotClass, namespace=namespace, print_output=True)
            except (InvalidConfigError, APIConnectionError):
                sys.exit(1)

        else:
            handleInvalidCommand()

    elif action in ("delete", "del", "rm"):
        # Get desired target from command line args
        target = getTarget(sys.argv)

        # Invoke desired action based on target
        if target in ("volume-snapshot", "volumesnapshot", "jupyterlab-snapshot", "jupyterlabsnapshot"):
            helpText = helpTextDeleteVolumeSnapshot
            if target in ("jupyterlab-snapshot", "jupyterlabsnapshot"):
                helpText = helpTextDeleteJupyterLabSnapshot

            snapshotName = None
            namespace = "default"
            force = False

            # Get command line options
            try:
                opts, args = getopt.getopt(sys.argv[3:], "hs:fn:", ["help", "snapshot-name=", "force", "namespace="])
            except:
                handleInvalidCommand(helpText=helpText, invalidOptArg=True)

            # Parse command line options
            for opt, arg in opts:
                if opt in ("-h", "--help"):
                    print(helpText)
                    sys.exit(0)
                elif opt in ("-s", "--snapshot-name"):
                    snapshotName = arg
                elif opt in ("-n", "--namespace"):
                    namespace = arg
                elif opt in ("-f", "--force"):
                    force = True

            # Check for required options
            if not snapshotName:
                handleInvalidCommand(helpText=helpText, invalidOptArg=True)

            # Confirm delete operation
            if not force:
                print("Warning: This snapshot will be permanently deleted.")
                while True:
                    proceed = input("Are you sure that you want to proceed? (yes/no): ")
                    if proceed in ("yes", "Yes", "YES"):
                        break
                    elif proceed in ("no", "No", "NO"):
                        sys.exit(0)
                    else:
                        print("Invalid value. Must enter 'yes' or 'no'.")

            # Delete snapshot
            try:
                delete_volume_snapshot(snapshot_name=snapshotName, namespace=namespace, print_output=True)
            except (InvalidConfigError, APIConnectionError):
                sys.exit(1)

        elif target in ("volume", "vol", "pvc", "persistentvolumeclaim"):
            pvcName = None
            namespace = "default"
            force = False
            preserveSnapshots = False

            # Get command line options
            try:
                opts, args = getopt.getopt(sys.argv[3:], "hp:fn:s",
                                           ["help", "pvc-name=", "force", "namespace=", "preserve-snapshots"])
            except:
                handleInvalidCommand(helpText=helpTextDeleteVolume, invalidOptArg=True)

            # Parse command line options
            for opt, arg in opts:
                if opt in ("-h", "--help"):
                    print(helpTextDeleteVolume)
                    sys.exit(0)
                elif opt in ("-p", "--pvc-name"):
                    pvcName = arg
                elif opt in ("-n", "--namespace"):
                    namespace = arg
                elif opt in ("-f", "--force"):
                    force = True
                elif opt in ("-s", "--preserve-snapshots"):
                    preserveSnapshots = True

            # Check for required options
            if not pvcName:
                handleInvalidCommand(helpText=helpTextDeleteVolume, invalidOptArg=True)

            # Confirm delete operation
            if not force:
                print("Warning: All data associated with the volume will be permanently deleted.")
                while True:
                    proceed = input("Are you sure that you want to proceed? (yes/no): ")
                    if proceed in ("yes", "Yes", "YES"):
                        break
                    elif proceed in ("no", "No", "NO"):
                        sys.exit(0)
                    else:
                        print("Invalid value. Must enter 'yes' or 'no'.")

            # Delete volume
            try:
                delete_volume(pvc_name=pvcName, namespace=namespace, preserve_snapshots=preserveSnapshots,
                              print_output=True)
            except (InvalidConfigError, APIConnectionError):
                sys.exit(1)

        elif target in ("jupyterlab", "jupyter"):
            workspaceName = None
            namespace = "default"
            force = False
            preserveSnapshots = False

            # Get command line options
            try:
                opts, args = getopt.getopt(sys.argv[3:], "hw:fn:s",
                                           ["help", "workspace-name=", "force", "namespace=", "preserve-snapshots"])
            except:
                handleInvalidCommand(helpText=helpTextDeleteJupyterLab, invalidOptArg=True)

            # Parse command line options
            for opt, arg in opts:
                if opt in ("-h", "--help"):
                    print(helpTextDeleteJupyterLab)
                    sys.exit(0)
                elif opt in ("-w", "--workspace-name"):
                    workspaceName = arg
                elif opt in ("-n", "--namespace"):
                    namespace = arg
                elif opt in ("-f", "--force"):
                    force = True
                elif opt in ("-s", "--preserve-snapshots"):
                    preserveSnapshots = True

            # Check for required options
            if not workspaceName:
                handleInvalidCommand(helpText=helpTextDeleteJupyterLab, invalidOptArg=True)

            # Confirm delete operation
            if not force:
                print("Warning: All data associated with the workspace will be permanently deleted.")
                while True:
                    proceed = input("Are you sure that you want to proceed? (yes/no): ")
                    if proceed in ("yes", "Yes", "YES"):
                        break
                    elif proceed in ("no", "No", "NO"):
                        sys.exit(0)
                    else:
                        print("Invalid value. Must enter 'yes' or 'no'.")

            # Delete JupyterLab workspace
            try:
                delete_jupyter_lab(workspace_name=workspaceName, namespace=namespace, preserve_snapshots=preserveSnapshots,
                                   print_output=True)
            except (InvalidConfigError, APIConnectionError):
                sys.exit(1)

        else:
            handleInvalidCommand()

    elif action in ("help", "h", "-h", "--help"):
        print(helpTextStandard)

    elif action in ("list", "ls"):
        # Get desired target from command line args
        target = getTarget(sys.argv)

        # Invoke desired action based on target
        if target in ("volume-snapshots", "volume-snapshot", "volumesnapshots", "volumesnapshot"):
            pvcName = None
            namespace = "default"

            # Get command line options
            try:
                opts, args = getopt.getopt(sys.argv[3:], "hp:n:", ["help", "pvc-name=", "namespace="])
            except:
                handleInvalidCommand(helpText=helpTextListVolumeSnapshots, invalidOptArg=True)

            # Parse command line options
            for opt, arg in opts:
                if opt in ("-h", "--help"):
                    print(helpTextListVolumeSnapshots)
                    sys.exit(0)
                elif opt in ("-p", "--pvc-name"):
                    pvcName = arg
                elif opt in ("-n", "--namespace"):
                    namespace = arg

            # List volumes
            try:
                list_volume_snapshots(pvc_name=pvcName, namespace=namespace, print_output=True)
            except (InvalidConfigError, APIConnectionError):
                sys.exit(1)

        elif target in (
        "volume", "vol", "volumes", "vols", "pvc", "persistentvolumeclaim", "pvcs", "persistentvolumeclaims"):
            namespace = "default"

            # Get command line options
            try:
                opts, args = getopt.getopt(sys.argv[3:], "hn:", ["help", "namespace="])
            except:
                handleInvalidCommand(helpText=helpTextListVolumes, invalidOptArg=True)

            # Parse command line options
            for opt, arg in opts:
                if opt in ("-h", "--help"):
                    print(helpTextListVolumes)
                    sys.exit(0)
                elif opt in ("-n", "--namespace"):
                    namespace = arg

            # List volumes
            try:
                list_volumes(namespace=namespace, print_output=True)
            except (InvalidConfigError, APIConnectionError):
                sys.exit(1)

        elif target in ("jupyterlab-snapshots", "jupyterlab-snapshot", "jupyterlabsnapshots", "jupyterlabsnapshot"):
            workspaceName = None
            namespace = "default"

            # Get command line options
            try:
                opts, args = getopt.getopt(sys.argv[3:], "hw:n:", ["help", "workspace-name=", "namespace="])
            except:
                handleInvalidCommand(helpText=helpTextListJupyterLabSnapshots, invalidOptArg=True)

            # Parse command line options
            for opt, arg in opts:
                if opt in ("-h", "--help"):
                    print(helpTextListJupyterLabSnapshots)
                    sys.exit(0)
                elif opt in ("-w", "--workspace-name"):
                    workspaceName = arg
                elif opt in ("-n", "--namespace"):
                    namespace = arg

            # List JupyterLab snapshots
            try:
                list_jupyter_lab_snapshots(workspace_name=workspaceName, namespace=namespace, print_output=True)
            except (InvalidConfigError, APIConnectionError):
                sys.exit(1)

        elif target in ("jupyterlabs", "jupyters", "jupyterlab", "jupyter"):
            namespace = "default"

            # Get command line options
            try:
                opts, args = getopt.getopt(sys.argv[3:], "hn:", ["help", "namespace="])
            except:
                handleInvalidCommand(helpText=helpTextListJupyterLabs, invalidOptArg=True)

            # Parse command line options
            for opt, arg in opts:
                if opt in ("-h", "--help"):
                    print(helpTextListJupyterLabs)
                    sys.exit(0)
                elif opt in ("-n", "--namespace"):
                    namespace = arg

            # List JupyterLab workspaces
            try:
                list_jupyter_labs(namespace=namespace, print_output=True)
            except (InvalidConfigError, APIConnectionError):
                sys.exit(1)

        else:
            handleInvalidCommand()

    elif action in ("restore"):
        # Get desired target from command line args
        target = getTarget(sys.argv)

        # Invoke desired action based on target
        if target in ("volume-snapshot", "volumesnapshot"):
            snapshotName = None
            namespace = "default"
            force = False

            # Get command line options
            try:
                opts, args = getopt.getopt(sys.argv[3:], "hs:fn:", ["help", "snapshot-name=", "force", "namespace="])
            except:
                handleInvalidCommand(helpText=helpTextRestoreVolumeSnapshot, invalidOptArg=True)

            # Parse command line options
            for opt, arg in opts:
                if opt in ("-h", "--help"):
                    print(helpTextRestoreVolumeSnapshot)
                    sys.exit(0)
                elif opt in ("-s", "--snapshot-name"):
                    snapshotName = arg
                elif opt in ("-n", "--namespace"):
                    namespace = arg
                elif opt in ("-f", "--force"):
                    force = True

            # Check for required options
            if not snapshotName:
                handleInvalidCommand(helpText=helpTextRestoreVolumeSnapshot, invalidOptArg=True)

            # Confirm restore operation
            if not force:
                print(
                    "Warning: In order to restore a snapshot, the PersistentVolumeClaim (PVC) associated the snapshot must NOT be mounted to any pods.")
                while True:
                    proceed = input("Are you sure that you want to proceed? (yes/no): ")
                    if proceed in ("yes", "Yes", "YES"):
                        break
                    elif proceed in ("no", "No", "NO"):
                        sys.exit(0)
                    else:
                        print("Invalid value. Must enter 'yes' or 'no'.")

            # Restore snapshot
            try:
                restore_volume_snapshot(snapshot_name=snapshotName, namespace=namespace, print_output=True)
            except (InvalidConfigError, APIConnectionError):
                sys.exit(1)

        elif target in ("jupyterlab-snapshot", "jupyterlabsnapshot"):
            snapshotName = None
            namespace = "default"

            # Get command line options
            try:
                opts, args = getopt.getopt(sys.argv[3:], "hs:n:", ["help", "snapshot-name=", "namespace="])
            except:
                handleInvalidCommand(helpText=helpTextRestoreJupyterLabSnapshot, invalidOptArg=True)

            # Parse command line options
            for opt, arg in opts:
                if opt in ("-h", "--help"):
                    print(helpTextRestoreJupyterLabSnapshot)
                    sys.exit(0)
                elif opt in ("-s", "--snapshot-name"):
                    snapshotName = arg
                elif opt in ("-n", "--namespace"):
                    namespace = arg

            # Check for required options
            if not snapshotName:
                handleInvalidCommand(helpText=helpTextRestoreJupyterLabSnapshot, invalidOptArg=True)

            # Restore snapshot
            try:
                restore_jupyter_lab_snapshot(snapshot_name=snapshotName, namespace=namespace, print_output=True)
            except (InvalidConfigError, APIConnectionError):
                sys.exit(1)

        else:
            handleInvalidCommand()

    elif action in ("version", "v", "-v", "--version"):
        print("NetApp DataOps Toolkit for Kubernetes - version " + k8s.__version__)

    else:
        handleInvalidCommand()
